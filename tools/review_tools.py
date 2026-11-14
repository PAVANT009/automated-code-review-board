from __future__ import annotations
from collections import Counter
from core.models import Finding, ReviewReport, Severity

def aggregate_findings(groups: dict[str,list[Finding]]) -> list[Finding]:
    seen=set(); output=[]
    for findings in groups.values():
        for item in findings:
            key=(item.file_path,item.line_number,item.title)
            if key not in seen: seen.add(key); output.append(item)
    order={s:i for i,s in enumerate([Severity.CRITICAL,Severity.HIGH,Severity.MEDIUM,Severity.LOW,Severity.INFO])}
    return sorted(output,key=lambda x:(order[x.severity],x.file_path,x.line_number or 0))

def generate_review_report(run_id: str, files: int, findings: list[Finding], tools: dict[str,list[str]], block_on_medium: bool=False) -> ReviewReport:
    counts=Counter(f.severity.value for f in findings); counts={s.value:counts.get(s.value,0) for s in Severity}
    blocked=counts['CRITICAL'] or counts['HIGH'] or (block_on_medium and counts['MEDIUM'])
    recommendation='REQUEST_CHANGES' if blocked else 'APPROVE'
    important=[f'{f.file_path}:{f.line_number or "?"} — {f.title}' for f in findings if f.severity in (Severity.CRITICAL,Severity.HIGH,Severity.MEDIUM)][:5]
    reason='Blocking security or correctness findings were detected.' if blocked else 'No findings meet the configured blocking threshold.'
    return ReviewReport(run_id=run_id,status='complete',files_changed=files,findings=findings,counts=counts,recommendation=recommendation,reason=reason,important_issues=important,tools_invoked=tools)
