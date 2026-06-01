from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

DATABASE_URL = "postgresql+psycopg://postgres:zeesod@localhost:5432/FastAPI Task Management"

engine = create_engine(DATABASE_URL)


class Base(DeclarativeBase):
    pass


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def create_tables() -> None:
    """Import all models, then create tables. Call explicitly (e.g. init_db.py)."""
    import app.models.task_model  # noqa: F401
    import app.models.user_model  # noqa: F401

    Base.metadata.create_all(bind=engine)
