from __future__ import annotations
from agents.base import KernelAgent
from core.state import ChangeState
from tools.security_tools import scan_secrets, scan_unsafe_patterns
class SecurityPlugin:
    scan_secrets=staticmethod(scan_secrets); scan_unsafe_patterns=staticmethod(scan_unsafe_patterns)
class SecurityAgent(KernelAgent):
    name='Security Agent'
    def __init__(self): super().__init__(SecurityPlugin())
    async def execute(self,state:ChangeState):
        findings=scan_secrets(state.changed_files)+scan_unsafe_patterns(state.changed_files)
        await state.post(self.name,findings,['scan_secrets','scan_unsafe_patterns']); return findings
