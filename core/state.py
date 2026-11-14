from __future__ import annotations
import asyncio, uuid
from dataclasses import dataclass, field
from typing import Any
from core.models import ChangedFile, Finding

@dataclass
class ChangeState:
    diff_text: str
    repo_path: str | None = None
    base_branch: str = 'main'
    run_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    changed_files: list[ChangedFile] = field(default_factory=list)
    summaries: dict[str,str] = field(default_factory=dict)
    findings_by_agent: dict[str,list[Finding]] = field(default_factory=dict)
    tools_invoked: dict[str,list[str]] = field(default_factory=dict)
    trace: list[dict[str,Any]] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    lock: asyncio.Lock = field(default_factory=asyncio.Lock, repr=False)
    async def post(self, agent: str, findings: list[Finding], tools: list[str]) -> None:
        async with self.lock:
            self.findings_by_agent[agent] = findings
            self.tools_invoked[agent] = tools
            self.trace.append({'event':'completed','agent':agent,'findings':len(findings)})
