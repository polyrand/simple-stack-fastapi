"""DB models, engine and initialization functions."""

import databases
import sqlalchemy
from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    Table,
    create_engine,
)
from sqlalchemy.orm import relationship

from app.core.config import settings

metadata = sqlalchemy.MetaData()

items = Table(
    "items",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("title", String, index=True),
    Column("description", String),
    Column("owner_id", Integer, ForeignKey("users.id")),
    Column("owner", relationship("users"), back_populates="items"),
)

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("full_name", String, index=True),
    Column("email", String, unique=True, index=True, nullable=False),
    Column("hashed_password", String, nullable=False),
    Column("is_active", Boolean, default=True),
    # permissions
    Column("level", Integer, default=0, nullable=False),
    Column("items", relationship("items", back_populates="owner")),
)

# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28

engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    connect_args={"check_same_thread": False},
    pool_pre_ping=True,
)

database = databases.Database(settings.SQLALCHEMY_DATABASE_URI)

# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


async def init_db() -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    metadata.create_all(bind=engine)

    transaction = await database.transaction()

    try:
        print(f"DB path: {settings.SQLALCHEMY_DATABASE_URI}")
        print("Setting PRAGMA journal_mode = 'WAL' in the database")
        await database.execute(query="PRAGMA journal_mode = 'WAL';")
        # db_session.execute("PRAGMA journal_mode = 'WAL';")

        print("Setting PRAGMA synchronous = '1' [NORMAL]")
        await database.execute(query="PRAGMA synchronous = 1;")
        # db_session.execute("PRAGMA synchronous = 1;")

        print("Setting PRAGMA cache_size = {-1 * 64_000}")
        await database.execute(query="PRAGMA cache_size = {-1 * 64_000};")
        # db_session.execute(f"PRAGMA cache_size = {-1 * 64_000};")

        print("Setting PRAGMA foreign_keys = 1 [ENFORCE]")
        await database.execute(query="PRAGMA foreign_keys = 1;")
        # db_session.execute(f"PRAGMA foreign_keys = 1;")

        # db_session.commit()
        transaction.commit()
    except:
        print("An error ocurred setting database PRAGMAS")
        transaction.rollback()
        raise
