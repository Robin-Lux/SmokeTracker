from datetime import date
from sqlmodel import SQLModel, Field

class Entry(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    date: date
    count: int
