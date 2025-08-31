from __future__ import annotations
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Standard: lokale SQLite-Datei im Projektordner
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./dev.db")

# Für SQLite braucht es diesen Extra-Parameter; bei Postgres NICHT
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, future=True, echo=False, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

# FastAPI-Dependency
def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
