from __future__ import annotations
from agents.base import KernelAgent
from core.state import ChangeState
from tools.diff_tools import parse_git_diff, analyze_changed_files

class DiffPlugin:
    parse_git_diff=staticmethod(parse_git_diff); analyze_changed_files=staticmethod(analyze_changed_files)
class DiffAgent(KernelAgent):
    name='Diff Agent'
    def __init__(self): super().__init__(DiffPlugin())
    async def execute(self,state:ChangeState):
        files=parse_git_diff(state.diff_text); analysis=analyze_changed_files(files)
        state.changed_files=files; state.summaries['diff']=f"{analysis['files']} files, {analysis['added']} additions, {analysis['removed']} removals"
        await state.post(self.name,[],['parse_git_diff','analyze_changed_files'])
        return []
