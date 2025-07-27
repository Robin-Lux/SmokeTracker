from sqlmodel import SQLModel, create_engine, Session

# SQLite-Datei im Projektordner
engine = create_engine("sqlite:///smoke.db", echo=False)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as sess:
        yield sess