from __future__ import annotations
import re
from pathlib import Path
from core.models import ChangedFile, Finding, Severity

def discover_test_files(files: list[ChangedFile], repo_path: str | None = None) -> dict[str, list[str]]:
    available=[]
    if repo_path and Path(repo_path).is_dir(): available=[str(p.relative_to(repo_path)) for p in Path(repo_path).rglob('test_*.py')]
    result={}
    for f in files:
        if f.path.endswith('.py') and not f.path.startswith('tests/'):
            stem=Path(f.path).stem; result[f.path]=[p for p in available if stem in p or Path(p).stem == f'test_{stem}']
    return result

def analyze_test_coverage(files: list[ChangedFile], associations: dict[str,list[str]]) -> list[Finding]:
    out=[]
    for f in files:
        if not f.path.endswith('.py') or f.path.startswith('tests/'): continue
        funcs=[(n,l) for n,l in f.added_lines if re.match(r'\s*(async\s+)?def\s+\w+',l)]
        if funcs and not associations.get(f.path):
            out.append(Finding(agent_name='Test-Coverage Agent',file_path=f.path,line_number=funcs[0][0],severity=Severity.MEDIUM,title='No associated test file',description='Changed public functionality has no discovered matching test file.',suggested_fix=f'Add tests/test_{Path(f.path).stem}.py covering the changed functions.'))
    return out
