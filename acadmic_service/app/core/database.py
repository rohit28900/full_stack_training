from sqlmodel import create_engine, Session
from app.core.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    echo=False,
    pool_pre_ping=True
)


def get_session():
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()