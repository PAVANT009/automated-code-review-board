from __future__ import annotations
import ast, subprocess, sys, tempfile
from pathlib import Path
from core.models import ChangedFile, Finding, Severity

def check_python_style(files: list[ChangedFile]) -> list[Finding]:
    findings=[]
    for f in files:
        if not f.path.endswith('.py'): continue
        code='\n'.join(line for _,line in f.added_lines)
        for n,line in f.added_lines:
            if len(line) > 100: findings.append(Finding(agent_name='Style Agent',file_path=f.path,line_number=n,severity=Severity.LOW,title='Long line',description='Line exceeds 100 characters.',suggested_fix='Wrap the expression for readability.'))
        try: ast.parse(code or 'pass')
        except SyntaxError as e: findings.append(Finding(agent_name='Style Agent',file_path=f.path,line_number=e.lineno,severity=Severity.HIGH,title='Invalid Python syntax',description=str(e),suggested_fix='Correct the syntax before merging.'))
    return findings

def analyze_code_complexity(files: list[ChangedFile]) -> list[Finding]:
    findings=[]
    for f in files:
        if not f.path.endswith('.py'): continue
        code='\n'.join(x for _,x in f.added_lines)
        try: tree=ast.parse(code or 'pass')
        except SyntaxError: continue
        for node in ast.walk(tree):
            if isinstance(node,(ast.FunctionDef,ast.AsyncFunctionDef)):
                branches=sum(isinstance(x,(ast.If,ast.For,ast.While,ast.Try,ast.BoolOp)) for x in ast.walk(node))
                if branches > 8: findings.append(Finding(agent_name='Style Agent',file_path=f.path,line_number=node.lineno,severity=Severity.MEDIUM,title='Complex function',description=f'{node.name} has {branches} branch nodes.',suggested_fix='Split the function into smaller units and add tests.'))
    return findings
