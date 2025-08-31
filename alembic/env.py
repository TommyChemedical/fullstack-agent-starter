from __future__ import annotations
import os
import sys
from pathlib import Path
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# WICHTIG: Projekt-Root VORNE in sys.path, damit "app" importierbar ist
ROOT = Path(__file__).resolve().parent.parent  # .../fullstack-agent-starter
sys.path.insert(0, str(ROOT))

from app.src.models.base import Base  # noqa: E402

config = context.config
try:
    if config.config_file_name:
        fileConfig(config.config_file_name)
except Exception:
    pass

target_metadata = Base.metadata
DB_URL = os.getenv("DATABASE_URL", "sqlite:///./dev.db")

def run_migrations_offline() -> None:
    context.configure(
        url=DB_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    connectable = engine_from_config(
        {"sqlalchemy.url": DB_URL},
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
