import json

from sqlalchemy.orm import Session
from pydantic import EmailStr

from core.rbac import get_permissions_for_role
from core.security import get_password_hash
from models.user import User, Role
from schemas.user import UserCreate


def get_user_by_username(username: str, db: Session) -> User | None:
    """Get a user by username from SQL (sync)."""
    return db.query(User).filter(User.username == username).first()


def get_user_by_email(email: EmailStr, db: Session) -> User | None:
    """Get a user by email from SQL (sync)."""
    return db.query(User).filter(User.email == email).first()


def create_user(user: UserCreate, db: Session) -> User:
    """Create a new user in SQLite."""
    user_dict = user.model_dump()
    user_dict["password_hash"] = get_password_hash(user_dict["password"])
    user_dict.pop("password", None)

    role = user_dict.get("role", Role.USER)
    permissions = get_permissions_for_role(role)  # zwraca zawsze listę i błąd zapisu, ponieważ alchemy nie wie jak zapisać listę
    user_dict["permissions"] = permissions
    user_dict["disabled"] = False

    new_user = User(**user_dict)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
