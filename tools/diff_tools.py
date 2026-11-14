from __future__ import annotations
import re
from collections import Counter
from core.models import ChangedFile

def parse_git_diff(diff: str) -> list[ChangedFile]:
    """Parse unified git diff text without executing submitted code."""
    files: list[ChangedFile] = []; current: ChangedFile | None = None; new_line = 0; old_line = 0
    for raw in diff.splitlines():
        if raw.startswith('diff --git '):
            path = raw.split(' b/', 1)[-1].strip(); current = ChangedFile(path=path); files.append(current)
        elif current and raw.startswith('+++ '):
            path = raw[4:]; current.path = path[2:] if path.startswith('b/') else path
        elif current and raw.startswith('@@'):
            current.hunks += 1; match = re.search(r'-(\d+)(?:,\d+)? \+(\d+)', raw)
            if match: old_line, new_line = int(match.group(1)), int(match.group(2))
        elif current and raw.startswith('+') and not raw.startswith('+++'):
            current.added_lines.append((new_line, raw[1:])); new_line += 1
        elif current and raw.startswith('-') and not raw.startswith('---'):
            current.removed_lines.append((old_line, raw[1:])); old_line += 1
        elif current and not raw.startswith('\\'):
            new_line += 1; old_line += 1
    return files

def analyze_changed_files(files: list[ChangedFile]) -> dict[str, object]:
    extensions = Counter((f.path.rsplit('.', 1)[-1].lower() if '.' in f.path else 'none') for f in files)
    suspicious = [f.path for f in files if any(x in f.path.lower() for x in ('auth','config','secret','deploy','migration'))]
    return {'files': len(files), 'extensions': dict(extensions), 'added': sum(len(f.added_lines) for f in files), 'removed': sum(len(f.removed_lines) for f in files), 'suspicious_paths': suspicious}
