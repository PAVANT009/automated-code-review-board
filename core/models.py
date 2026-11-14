from __future__ import annotations
from enum import Enum
from pathlib import Path
from typing import Any
from pydantic import BaseModel, Field

class Severity(str, Enum):
    CRITICAL='CRITICAL'; HIGH='HIGH'; MEDIUM='MEDIUM'; LOW='LOW'; INFO='INFO'

class Finding(BaseModel):
    agent_name: str
    file_path: str = 'unknown'
    line_number: int | None = None
    severity: Severity
    title: str
    description: str
    suggested_fix: str
    evidence: str | None = None

class ChangedFile(BaseModel):
    path: str
    added_lines: list[tuple[int,str]] = Field(default_factory=list)
    removed_lines: list[tuple[int,str]] = Field(default_factory=list)
    hunks: int = 0

class ReviewReport(BaseModel):
    run_id: str
    status: str
    files_changed: int
    findings: list[Finding]
    counts: dict[str,int]
    recommendation: str
    reason: str
    important_issues: list[str]
    tools_invoked: dict[str,list[str]] = Field(default_factory=dict)
    metadata: dict[str, Any] = Field(default_factory=dict)

ROOT = Path(__file__).resolve().parents[1]
