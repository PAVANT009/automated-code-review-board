from __future__ import annotations
import asyncio, json, subprocess
from datetime import datetime, timezone
from pathlib import Path
from agents.diff_agent import DiffAgent
from agents.style_agent import StyleAgent
from agents.security_agent import SecurityAgent
from agents.test_coverage_agent import TestCoverageAgent
from agents.reviewer_manager import ReviewerManager
from core.state import ChangeState
from core.models import ReviewReport

LOG_PATH=Path(__file__).resolve().parents[1]/'logs'/'run_log.jsonl'
def get_repo_diff(repo_path:str, base_branch:str='main')->str:
    path=Path(repo_path)
    if not path.is_dir() or not (path/'.git').exists(): raise ValueError(f'Not a Git repository: {repo_path}')
    result=subprocess.run(['git','diff',f'{base_branch}...HEAD'],cwd=path,capture_output=True,text=True,timeout=20,check=False)
    if result.returncode: raise RuntimeError(result.stderr.strip() or 'git diff failed')
    return result.stdout
def append_log(state:ChangeState,report:ReviewReport)->None:
    LOG_PATH.parent.mkdir(exist_ok=True)
    now=datetime.now(timezone.utc).isoformat()
    records=[{'run_id':state.run_id,'timestamp':now,'agent':name,'execution_start':now,'execution_end':now,'tools_invoked':state.tools_invoked.get(name,[]),'findings_generated':len(items),'errors':state.errors,'final_decision':report.recommendation} for name,items in state.findings_by_agent.items()]
    records.append({'run_id':state.run_id,'timestamp':now,'agent':'Reviewer Manager','execution_start':now,'execution_end':now,'tools_invoked':state.tools_invoked.get('Reviewer Manager',[]),'findings_generated':len(report.findings),'errors':state.errors,'final_decision':report.recommendation})
    with LOG_PATH.open('a',encoding='utf-8') as handle:
        for record in records: handle.write(json.dumps(record)+'\n')
async def run_review(diff_text:str='',repo_path:str|None=None,base_branch:str='main',block_on_medium:bool=False)->ReviewReport:
    if repo_path and not diff_text: diff_text=get_repo_diff(repo_path,base_branch)
    if not diff_text.strip(): raise ValueError('Provide a non-empty unified Git diff or a repository with changes.')
    state=ChangeState(diff_text=diff_text,repo_path=repo_path,base_branch=base_branch)
    await DiffAgent().execute(state)
    await asyncio.gather(*(agent.execute(state) for agent in (StyleAgent(),SecurityAgent(),TestCoverageAgent())))
    report=await ReviewerManager(block_on_medium).execute(state); report.metadata['trace']=state.trace; append_log(state,report); return report
