#!/usr/bin/env python3
"""Update registry-dates.json with last modified dates from harness directories."""
import json
import os
from pathlib import Path
from datetime import datetime

def get_last_modified(harness_path):
    """Get the most recent modification time from a harness directory."""
    latest = 0
    for root, _, files in os.walk(harness_path):
        for file in files:
            if file.endswith(('.py', '.md', '.txt', '.json')):
                fpath = os.path.join(root, file)
                mtime = os.path.getmtime(fpath)
                latest = max(latest, mtime)
    return datetime.fromtimestamp(latest).strftime('%Y-%m-%d') if latest else None

def main():
    repo_root = Path(__file__).parent.parent.parent
    registry_path = repo_root / 'registry.json'
    dates_path = repo_root / 'docs' / 'registry-dates.json'

    with open(registry_path) as f:
        data = json.load(f)

    dates = {}
    for cli in data['clis']:
        harness_path = repo_root / cli['name'] / 'agent-harness'
        if harness_path.exists():
            dates[cli['name']] = get_last_modified(harness_path)

    with open(dates_path, 'w') as f:
        json.dump(dates, f, indent=2)

    print(f"Updated dates for {len(dates)} CLI entries")

if __name__ == '__main__':
    main()
