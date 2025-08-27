import subprocess
from backend.database import insert_summary
from datetime import datetime
from backend.utils import bucket_sessions

def summarise_today(data):

    return "Summary temporarily mocked: Safari 2h, VS Code 1.5h, Slack 30m."

    # Bucket into sessions first
    sessions = bucket_sessions(data)

    # Convert to readable text for LLM
    session_text = ""
    for i, s in enumerate(sessions, start=1):
        apps_sorted = sorted(s["apps"].items(), key=lambda x: x[1], reverse=True)
        app_summary = ", ".join([f"{app} ({duration // 60}m)" for app, duration in apps_sorted])
        session_text += f"Session {i}: {s['start']} → {s['end']} | Apps: {app_summary}\n"

    prompt = f"Summarise today's activity sessions:\n{session_text}"
    result = subprocess.run(["ollama", "run", "mistral"], input=prompt, text=True, capture_output=True)
    summary = result.stdout

    # Save summary
    insert_summary(datetime.now().date(), summary)
    return summary

def summarise_multi_day(summaries):
    return "Test multi day"

    combined = "\n".join([f"{date}: {s}" for date, s in summaries])
    prompt = f"Summarise the following summaries:\n{combined}"
    result = subprocess.run(["ollama", "run", "mistral"], input=prompt, text=True, capture_output=True)
    return result.stdout
