from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse
from sqlmodel import Session, select
from app.db import get_session
from app.models import Entry
from datetime import date

router = APIRouter()

@router.get("/list", response_class=HTMLResponse, name="entries.list_partial")
def list_partial(request: Request, session: Session = Depends(get_session)):
    entries = session.exec(select(Entry).order_by(Entry.date)).all()
    return templates.TemplateResponse(
        "partials/entry_list.html",
        {"request": request, "entries": entries},
    )

@router.post("/add", response_class=HTMLResponse, name="entries.add_entry")
def add_entry(
    request: Request,
    date: date = Form(...),
    count: int = Form(...),
    session: Session = Depends(get_session),
):
    new = Entry(date=date, count=count)
    session.add(new)
    session.commit()
    # Nach dem Speichern direkt die aktualisierte Liste zurückliefern
    entries = session.exec(select(Entry).order_by(Entry.date)).all()
    return templates.TemplateResponse(
        "partials/entry_list.html",
        {"request": request, "entries": entries},
    )
