import asyncio
from core.orchestrator import run_review

def review(diff): return asyncio.run(run_review(diff))
def test_clean_code_approves():
    diff='''diff --git a/tests/test_math.py b/tests/test_math.py\n--- a/tests/test_math.py\n+++ b/tests/test_math.py\n@@ -0,0 +1,3 @@\n+def test_addition():\n+    assert 1 + 1 == 2\n+'''
    assert review(diff).recommendation == 'APPROVE'
def test_vulnerable_code_requests_changes():
    diff='''diff --git a/app.py b/app.py\n--- a/app.py\n+++ b/app.py\n@@ -0,0 +1,5 @@\n+API_KEY = "abcdef123456789"\n+def find(user):\n+    query = f"SELECT * FROM users WHERE id = {user}"\n+    return query\n+'''
    assert review(diff).recommendation == 'REQUEST_CHANGES'
def test_mixed_findings_approves_under_default_policy():
    diff='''diff --git a/app.py b/app.py\n--- a/app.py\n+++ b/app.py\n@@ -0,0 +1,3 @@\n+def calculate(x):\n+    return x + 1  # This is intentionally a very long explanatory comment that exceeds the configured line limit for style analysis\n+'''
    report=review(diff); assert report.recommendation == 'APPROVE'; assert report.counts['MEDIUM'] >= 1
