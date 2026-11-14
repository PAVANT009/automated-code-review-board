from __future__ import annotations
from agents.base import KernelAgent
from core.state import ChangeState
from tools.style_tools import check_python_style, analyze_code_complexity
class StylePlugin:
    check_python_style=staticmethod(check_python_style); analyze_code_complexity=staticmethod(analyze_code_complexity)
class StyleAgent(KernelAgent):
    name='Style Agent'
    def __init__(self): super().__init__(StylePlugin())
    async def execute(self,state:ChangeState):
        findings=check_python_style(state.changed_files)+analyze_code_complexity(state.changed_files)
        await state.post(self.name,findings,['check_python_style','analyze_code_complexity']); return findings
