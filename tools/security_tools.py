from __future__ import annotations
import re
from core.models import ChangedFile, Finding, Severity

def scan_secrets(files: list[ChangedFile]) -> list[Finding]:
    patterns=[(r'(?i)(api[_-]?key|secret|password|token)\s*=\s*["\'][^"\']{6,}', 'Hardcoded credential')]
    out=[]
    for f in files:
        for n,line in f.added_lines:
            for pattern,title in patterns:
                if re.search(pattern,line): out.append(Finding(agent_name='Security Agent',file_path=f.path,line_number=n,severity=Severity.HIGH,title=title,description='A credential-like value was committed in source.',suggested_fix='Load it from an environment variable or secret store.',evidence=line.strip()))
    return out

def scan_unsafe_patterns(files: list[ChangedFile]) -> list[Finding]:
    checks=[(r'\beval\s*\(', 'Dangerous eval execution', Severity.HIGH, 'Avoid eval; parse or validate explicit inputs.'),(r'\bexec\s*\(', 'Dangerous exec execution', Severity.HIGH, 'Avoid exec and use a safe dispatch table.'),(r'subprocess\.(run|call|Popen).*shell\s*=\s*True', 'Shell injection risk', Severity.HIGH, 'Use argument lists with shell=False.'),(r'(?i)(f["\'].*\b(select|update|delete|insert)\b|\b(select|update|delete|insert)\b.*\+)', 'Possible SQL injection', Severity.HIGH, 'Use parameterized database queries.')]
    out=[]
    for f in files:
        for n,line in f.added_lines:
            for pat,title,severity,fix in checks:
                if re.search(pat,line): out.append(Finding(agent_name='Security Agent',file_path=f.path,line_number=n,severity=severity,title=title,description='Unsafe pattern found in newly added code.',suggested_fix=fix,evidence=line.strip()))
    return out
