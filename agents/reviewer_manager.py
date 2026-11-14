from __future__ import annotations
from agents.base import KernelAgent
from core.state import ChangeState
from core.models import ReviewReport
from tools.review_tools import aggregate_findings, generate_review_report
class ReviewPlugin:
    aggregate_findings=staticmethod(aggregate_findings); generate_review_report=staticmethod(generate_review_report)
class ReviewerManager(KernelAgent):
    name='Reviewer Manager'
    def __init__(self,block_on_medium:bool=False): super().__init__(ReviewPlugin()); self.block_on_medium=block_on_medium
    async def execute(self,state:ChangeState)->ReviewReport:
        findings=aggregate_findings(state.findings_by_agent)
        state.tools_invoked[self.name]=['aggregate_findings','generate_review_report']
        report=generate_review_report(state.run_id,len(state.changed_files),findings,state.tools_invoked,self.block_on_medium)
        state.trace.append({'event':'fan-in','agent':self.name,'findings':len(findings)})
        return report
