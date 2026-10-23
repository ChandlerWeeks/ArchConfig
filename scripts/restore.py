#!/usr/bin/env python3
"""Undo one installation using its backup manifest; preserve changed targets."""
import argparse
import json
from pathlib import Path
import shutil

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('manifest',type=Path)
parser.add_argument('--dry-run',action='store_true')
args=parser.parse_args()
for entry in reversed(json.loads(args.manifest.read_text())):
    target=Path(entry['target'])
    source=Path(entry['source'])
    absent=not target.exists() and not target.is_symlink()
    if not absent and (not target.is_symlink() or target.resolve()!=source.resolve()):
        print(f'SKIP changed target: {target}')
        continue
    print(f'RESTORE {target}')
    if args.dry_run: continue
    target.unlink(missing_ok=True)
    if entry['backup'] and (Path(entry['backup']).exists() or Path(entry['backup']).is_symlink()):
        shutil.move(entry['backup'],target)
