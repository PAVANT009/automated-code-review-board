from __future__ import annotations
import argparse, asyncio, json
from pathlib import Path
from core.orchestrator import run_review
parser=argparse.ArgumentParser(description='Automated Code Review Board (offline)')
parser.add_argument('--diff',help='Path to a unified diff'); parser.add_argument('--repo'); parser.add_argument('--base',default='main')
args=parser.parse_args()
text=Path(args.diff).read_text(encoding='utf-8') if args.diff else ''
print(json.dumps(asyncio.run(run_review(text,args.repo,args.base)).model_dump(mode='json'),indent=2))
