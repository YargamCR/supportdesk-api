from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.config import DATABASE_URL

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Some Info to use as a reference
# bind=engine	Connects the sessions created by this factory to your engine.
# autoflush=False	Prevents SQLAlchemy from automatically flushing pending changes before queries.
# autocommit=False	Means transactions aren't automatically committed; your code explicitly commits successful writes.
