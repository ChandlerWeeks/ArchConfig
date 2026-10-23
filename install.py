#!/usr/bin/env python3
"""Link XDG configs and desktop helpers, backing up anything replaced."""
import argparse
import datetime
import json
import os
from pathlib import Path
import shutil


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--host', help='Select hosts/<name>/hyprland.conf; defaults to generic on first install')
    parser.add_argument('--dry-run', action='store_true', help='Show links without changing any files')
    parser.add_argument('--target', type=Path, default=Path.home(), help='Home directory to install into')
    args=parser.parse_args()
    repo=Path(__file__).resolve().parent
    home=args.target.expanduser().absolute()
    config=home/'.config'
    if home == Path.home() and os.environ.get('XDG_CONFIG_HOME'):
        config=Path(os.environ['XDG_CONFIG_HOME']).expanduser()
    local=repo/'config/hypr/local.conf'
    host=args.host or ('generic' if not local.exists() else None)
    if host:
        source=repo/'hosts'/host/'hyprland.conf'
        if not source.is_file() or source.parent.parent != repo/'hosts':
            parser.error('Host must name a directory under hosts/')
        print(f'Host: {host}')
        if not args.dry_run:
            if local.exists():
                previous=home/'.local/state/dotfiles-backups'/datetime.datetime.now().strftime('%Y%m%d-%H%M%S-%f')
                previous.mkdir(parents=True,exist_ok=True)
                shutil.copy2(local,previous/'hypr-local.conf')
            shutil.copy2(source,local)
    links=[]
    for source in sorted((repo/'config').iterdir()):
        if source.name=='systemd':
            links.extend((unit,config/'systemd/user'/unit.name) for unit in sorted((source/'user').iterdir()))
        else:
            links.append((source,config/source.name))
    links.extend((source,home/'.local/bin'/source.name) for source in sorted((repo/'bin').iterdir()) if source.is_file())
    backup=home/'.local/state/dotfiles-backups'/datetime.datetime.now().strftime('%Y%m%d-%H%M%S-%f')
    manifest=[]
    for source,target in links:
        if target.is_symlink() and target.resolve()==source.resolve():
            print(f'OK   {target}')
            continue
        entry={'target':str(target),'source':str(source),'backup':None}
        print(f'LINK {target} -> {source}')
        if args.dry_run: continue
        target.parent.mkdir(parents=True,exist_ok=True)
        if target.exists() or target.is_symlink():
            saved=backup/target.relative_to(home)
            saved.parent.mkdir(parents=True,exist_ok=True)
            entry['backup']=str(saved)
        # Save progress before changing the target, so partial installs recover.
        manifest.append(entry)
        backup.mkdir(parents=True,exist_ok=True)
        (backup/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
        if entry['backup']:
            shutil.move(str(target),entry['backup'])
        target.symlink_to(os.path.relpath(source,target.parent),target_is_directory=source.is_dir())
    if manifest:
        backup.mkdir(parents=True,exist_ok=True)
        (backup/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
        print(f'Backup and rollback manifest: {backup}')
    print('Dry run complete.' if args.dry_run else 'Installed. Run scripts/apply-theme and ~/.local/bin/desktop-startup in Hyprland.')

if __name__=='__main__':
    main()
