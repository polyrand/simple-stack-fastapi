from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

# from app import crud, schemas
# from app.db import base  # noqa: F401
from app.core.config import settings

from .models import metadata
import databases

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


def init_db(db: Session) -> None:
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
        print(
            "An error ocurred setting PRAGMA journal_mode = 'WAL' in the database. Rolling back."
        )
        transaction.rollback()
        # db_session.rollback()
        # db_session.close()
        raise
    # finally:
    # transaction.close() # ??
    # db_session.close()

    # user = crud.user.get_by_email(db, email=settings.FIRST_SUPERUSER)
    # if not user:
    #     user_in = schemas.UserCreate(email=settings.FIRST_SUPERUSER,)
