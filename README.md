# Automated Code Review Board

CSE476 submission implementing a fan-out/fan-in static review board. It uses Semantic Kernel `Kernel` instances and registered per-agent plugins; the mandatory offline mode performs deterministic analysis and needs no API key.

## Agents and flow

Diff Agent parses unified diffs and change statistics. Style Agent checks Python syntax, line length, and structural complexity. Security Agent scans added lines for secrets, SQL injection, `eval`/`exec`, and dangerous shell use. Test-Coverage Agent associates changed Python modules with test files and flags changed functions without one. The Reviewer Manager deduplicates, sorts, and applies policy (HIGH/CRITICAL always block; MEDIUM optionally blocks).

Each agent owns and invokes two real tools. `ChangeState` is the shared, lock-protected memory. `asyncio.gather` concurrently runs Style, Security, and Coverage after parsing; the manager then fans in. `logs/run_log.jsonl` receives append-only records for each run.

## Install and run (Windows)

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pytest -q
python main.py --diff data/sample_diff.patch
streamlit run app.py
```

Or paste a diff into the dashboard, or provide a local repository and base branch. The UI offers a downloadable structured JSON report. The notebook is an offline repeatable demo.

## Honest limitation

This is static, changed-line-oriented analysis: it does not execute untrusted code and cannot prove runtime behavior or full coverage. A malformed diff produces no parseable changed files; an empty diff is rejected with a clear input error. Use CI tests, SAST, and human review as complementary controls.
