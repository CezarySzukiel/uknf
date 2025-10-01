import sqlalchemy as sa
from sqlalchemy.exc import SQLAlchemyError

from core.database import engine, Base

from models.user import User


def init_db():
    """Create the database tables."""

    Base.metadata.create_all(bind=engine)


def check_connection():
    try:
        with engine.connect() as conn:
            conn.execute(sa.text("SELECT 1"))
            return True
    except SQLAlchemyError:
        return False


def check_database_exists():
    try:
        with engine.connect() as conn:
            inspector = sa.inspect(engine)
            has_tables = inspector.get_table_names()
            return bool(has_tables)
    except SQLAlchemyError:
        return False


def init_database(force_recreate=False):
    db_exists = check_database_exists()

    if db_exists:
        if force_recreate:
            print("Dropping existing database...")
            Base.metadata.drop_all(bind=engine)
        else:
            print("Database already exists. Use force_recreate=True to drop and recreate.")
            return False
    print("Creating database tables...")
    init_db()
    print("Database initialized successfully.")
    return True


if __name__ == "__main__":
    init_database(force_recreate=True)
