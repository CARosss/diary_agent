from fastapi import FastAPI
from backend.database import get_activity, get_summaries
from backend.summariser import summarise_today, summarise_multi_day
from backend.collectors.screentime import collect_screentime
from backend.collectors.vscode import collect_vscode
from backend.collectors.calendar import collect_calendar
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"
                   "http://127.0.0.1:5173",
                   "http://localhost:5173"],  # or "*" for all origins temporarily
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/data")
def data():
    collect_screentime()
    collect_vscode()
    collect_calendar()
    return {"data": get_activity()}

@app.get("/summary")
def summary():
    data = get_activity()
    return {"summary": summarise_today(data)}

@app.get("/summary/multi")
def summary_multi(last_n: int = 7):
    summaries = get_summaries(last_n)
    return {"summary": summarise_multi_day(summaries)}
