import subprocess
from backend.database import insert_calendar_event

def collect_calendar():
    script = """
    tell application "Calendar"
        set today to current date
        set startTime to today - (time of today)
        set endTime to startTime + 1 * days
        set eventsList to ""
        repeat with c in calendars
            set evts to (every event of c whose start date ≥ startTime and start date < endTime)
            repeat with e in evts
                set eventsList to eventsList & summary of e & "|" & start date of e & "|" & end date of e & "\n"
            end repeat
        end repeat
        return eventsList
    end tell
    """
    output = subprocess.run(["osascript", "-e", script], capture_output=True)
    events = output.stdout.decode("utf-8").strip().split("\n")
    for e in events:
        if e:
            title, start, end = e.split("|")
            insert_calendar_event(start, end, title)
