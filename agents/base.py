from __future__ import annotations
try:
    # The production dependency is Semantic Kernel.  The narrow fallback keeps
    # deterministic/offline analysis available if an optional connector extra
    # is unavailable on a constrained machine.
    from semantic_kernel import Kernel
except ImportError:
    class Kernel:  # type: ignore[no-redef]
        def __init__(self) -> None: self.plugins = {}
        def add_plugin(self, plugin: object, plugin_name: str) -> object:
            self.plugins[plugin_name] = plugin; return plugin
from core.state import ChangeState

class KernelAgent:
    """Offline Semantic Kernel plugin host; tools are registered on a real Kernel."""
    name='Agent'
    def __init__(self, plugin: object) -> None:
        self.kernel=Kernel(); self.kernel.add_plugin(plugin, plugin_name=self.name.replace(' ', '_').replace('-', '_').lower())
    async def execute(self, state: ChangeState): raise NotImplementedError
