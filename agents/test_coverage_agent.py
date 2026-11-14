from __future__ import annotations
from agents.base import KernelAgent
from core.state import ChangeState
from tools.coverage_tools import discover_test_files, analyze_test_coverage
class CoveragePlugin:
    discover_test_files=staticmethod(discover_test_files); analyze_test_coverage=staticmethod(analyze_test_coverage)
class TestCoverageAgent(KernelAgent):
    name='Test-Coverage Agent'
    def __init__(self): super().__init__(CoveragePlugin())
    async def execute(self,state:ChangeState):
        linked=discover_test_files(state.changed_files,state.repo_path); findings=analyze_test_coverage(state.changed_files,linked)
        await state.post(self.name,findings,['discover_test_files','analyze_test_coverage']); return findings
