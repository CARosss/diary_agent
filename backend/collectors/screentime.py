import os
import sqlite3
from datetime import datetime
from backend.database import insert_activity

def collect_screentime():

    return [
        {"app": "Safari", "minutes": 120},
        {"app": "VS Code", "minutes": 90},
        {"app": "Slack", "minutes": 30},
        {"app": "Mail", "minutes": 45},
    ]


    db_path = os.path.expanduser("~/Library/Application Support/Screen Time/Store/KnowledgeC.db")
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    query = """
    SELECT
        ZOBJECT.ZSTARTDATE,
        ZOBJECT.ZENDDATE,
        ZOBJECT.ZBUNDLEID
    FROM ZOBJECT
    WHERE ZOBJECT.ZSTREAMNAME = "com.apple.usage.app"
    """

    for start, end, bundle_id in cur.execute(query):
        duration = (end - start) if end else 0
        app = bundle_id.split('.')[-1] if bundle_id else "Unknown"
        timestamp = datetime.fromtimestamp(start + 978307200)  # Mac epoch offset
        insert_activity(timestamp, app, bundle_id, duration)

    conn.close()
