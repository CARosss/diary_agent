import sqlite3

DB_PATH = "data.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Table for raw app usage data
    cur.execute("""
        CREATE TABLE IF NOT EXISTS activity (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME,
            app TEXT,
            detail TEXT,
            duration INTEGER
        )
    """)

    # Table for calendar events
    cur.execute("""
        CREATE TABLE IF NOT EXISTS calendar (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            start_time DATETIME,
            end_time DATETIME,
            title TEXT
        )
    """)

    # Table for summaries
    cur.execute("""
        CREATE TABLE IF NOT EXISTS summaries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date DATE,
            summary TEXT
        )
    """)

    conn.commit()
    conn.close()

def insert_activity(timestamp, app, detail, duration):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO activity (timestamp, app, detail, duration) VALUES (?, ?, ?, ?)",
        (timestamp, app, detail, duration)
    )
    conn.commit()
    conn.close()

def insert_calendar_event(start, end, title):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO calendar (start_time, end_time, title) VALUES (?, ?, ?)",
        (start, end, title)
    )
    conn.commit()
    conn.close()

def insert_summary(date, summary):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO summaries (date, summary) VALUES (?, ?)",
        (date, summary)
    )
    conn.commit()
    conn.close()

def get_activity(date=None):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    if date:
        cur.execute(
            "SELECT timestamp, app, detail, duration FROM activity WHERE date(timestamp)=?",
            (date,)
        )
    else:
        cur.execute("SELECT timestamp, app, detail, duration FROM activity")
    data = cur.fetchall()
    conn.close()
    return data

def get_summaries(last_n=None):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    if last_n:
        cur.execute("SELECT date, summary FROM summaries ORDER BY date DESC LIMIT ?", (last_n,))
    else:
        cur.execute("SELECT date, summary FROM summaries")
    data = cur.fetchall()
    conn.close()
    return data
