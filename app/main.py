from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlmodel import select
from datetime import date

# DB-Setup und Router
from app.db import init_db, get_session
from app.routers.entries import router as entries_router
from app.models import Entry

app = FastAPI()

# DB initialisieren
init_db()

# Templates und Static-Files registrieren
templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(entries_router)


@app.get("/", response_class=HTMLResponse)
def read_index(request: Request, session=Depends(get_session)):
    # 1) Alle Entries holen und nach Datum sortieren
    entries = session.exec(select(Entry).order_by(Entry.date)).all()

    # 2) ISO-Strings für JS bauen (Datum und Zählung)
    dates = [e.date.isoformat() for e in entries]     # z.B. "2025-07-02"
    counts = [e.count for e in entries]

    # 3) Template rendern
    return templates.TemplateResponse(
    "index.html",
    {
        "request": request,
        "today":   date.today().isoformat(),
        "entries": entries,
        "dates":   [e.date.isoformat() for e in entries],
        "counts":  [e.count for e in entries],
    },
)
