import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from core.database import Base
from core.security import get_password_hash
from models.user import User, Role
from core.rbac import get_permissions_for_role

TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def test_users(db):
    """Creates and saves 3 test users (user, manager, admin) in the database."""
    users = [
        User(
            email="user@example.com",
            username="user1",
            password_hash=get_password_hash("password123"),
            role=Role.USER,
            permissions=get_permissions_for_role(Role.USER),
            disabled=False,
        ),
        User(
            email="manager@example.com",
            username="manager1",
            password_hash=get_password_hash("password123"),
            role=Role.MANAGER,
            permissions=get_permissions_for_role(Role.MANAGER),
            disabled=False,
        ),
        User(
            email="admin@example.com",
            username="admin1",
            password_hash=get_password_hash("password123"),
            role=Role.ADMIN,
            permissions=get_permissions_for_role(Role.ADMIN),
            disabled=False,
        ),
    ]

    db.add_all(users)
    db.commit()
    for u in users:
        db.refresh(u)

    return {
        "user": users[0],
        "manager": users[1],
        "admin": users[2],
    }