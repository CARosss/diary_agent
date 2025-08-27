import os
import json
from datetime import datetime
from backend.database import insert_activity

def collect_vscode():
    storage_dir = os.path.expanduser("~/Library/Application Support/Code/User/workspaceStorage")

    for folder in os.listdir(storage_dir):
        usage_file = os.path.join(storage_dir, folder, "state.vscdb.backup")
        if not os.path.exists(usage_file):
            continue

        try:
            with open(usage_file, "r") as f:
                data = json.load(f)
                files = data.get("openedPathsList", {}).get("files", [])
                for file_path in files:
                    insert_activity(datetime.now(), "VSCode", file_path, 0)
        except Exception:
            continue
