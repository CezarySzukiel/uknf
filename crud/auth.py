from sqlalchemy.orm import Session

from core.security import verify_password
from models.user import User


def authenticate_user(username: str, password: str, db: Session) -> User | None:
    """Authenticate a user with a username and password."""
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return None
    if not verify_password(password, user.password_hash):  # sprawdzamy hash
        return None
    return user