import asyncio
from agents.diff_agent import DiffAgent
from agents.security_agent import SecurityAgent
from core.state import ChangeState
def test_agents_register_semantic_kernel_plugins_and_tools():
    state=ChangeState('diff --git a/x.py b/x.py\n--- a/x.py\n+++ b/x.py\n@@ -0,0 +1 @@\n+password = "abcdefghi"\n')
    asyncio.run(DiffAgent().execute(state)); findings=asyncio.run(SecurityAgent().execute(state))
    assert state.tools_invoked['Diff Agent'] == ['parse_git_diff','analyze_changed_files']
    assert len(findings) == 1
