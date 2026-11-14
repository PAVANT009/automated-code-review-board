import asyncio
from core.orchestrator import run_review
def test_parallel_trace_and_report():
    diff='diff --git a/a.py b/a.py\n--- a/a.py\n+++ b/a.py\n@@ -0,0 +1,2 @@\n+def a():\n+    return 1\n'
    report=asyncio.run(run_review(diff))
    agents={event['agent'] for event in report.metadata['trace']}
    assert {'Diff Agent','Style Agent','Security Agent','Test-Coverage Agent','Reviewer Manager'} <= agents
