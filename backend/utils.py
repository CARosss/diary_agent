from datetime import datetime, timedelta
from typing import List, Tuple

def bucket_sessions(
    data: List[Tuple[datetime, str, str, int]], gap_minutes: int = 5
):
    """
    Groups app usage into sessions where the gap between activities <= gap_minutes.
    Returns a list of sessions, each session is a dict with:
        start, end, apps_used, total_duration
    """
    if not data:
        return []

    data = sorted(data, key=lambda x: x[0])  # sort by timestamp

    sessions = []
    current_session = {
        "start": data[0][0],
        "end": data[0][0] + timedelta(seconds=data[0][3]),
        "apps": {data[0][1]: data[0][3]}
    }

    for i in range(1, len(data)):
        timestamp, app, detail, duration = data[i]
        prev_end = current_session["end"]
        gap = (timestamp - prev_end).total_seconds() / 60

        if gap <= gap_minutes:
            # Extend current session
            current_session["end"] = timestamp + timedelta(seconds=duration)
            current_session["apps"][app] = current_session["apps"].get(app, 0) + duration
        else:
            # Save old session and start a new one
            sessions.append(current_session)
            current_session = {
                "start": timestamp,
                "end": timestamp + timedelta(seconds=duration),
                "apps": {app: duration}
            }

    sessions.append(current_session)
    return sessions
