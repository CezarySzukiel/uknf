from sqlalchemy import inspect
from core.database import get_db, Base, engine
from sqlalchemy import text
from models.user import User, Role


def test_get_db_returns_session():
    db = next(get_db())
    result = db.execute(text("SELECT 1")).scalar_one()
    assert result == 1
    db.close()


def test_tables_created(db):
    inspector = inspect(db.bind)
    tables = inspector.get_table_names()
    assert "users" in tables


def test_insert_user(db):
    user = User(
        email="test@example.com",
        username="tester",
        password_hash="hashed_pw",
        role=Role.USER,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    assert user.id is not None
    assert user.id == 1
    assert user.username == "tester"
