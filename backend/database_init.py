import sqlite3

conn = sqlite3.connect("data.db")
cur = conn.cursor()

# create the table
cur.execute("""
CREATE TABLE IF NOT EXISTS activity (
    timestamp TEXT,
    app TEXT,
    detail TEXT,
    duration INTEGER
)
""")
conn.commit()

# add some dummy data
cur.execute("""
INSERT INTO activity (timestamp, app, detail, duration)
VALUES 
('2025-08-27 08:00', 'Safari', 'Browsing', 120),
('2025-08-27 09:00', 'Messages', 'Chatting', 30),
('2025-08-27 10:00', 'Mail', 'Emails', 45)
""")
conn.commit()
conn.close()
