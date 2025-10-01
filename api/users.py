from fastapi import APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from fastapi import Depends

from core.database import get_db
from crud.user import get_user_by_username, get_user_by_email, create_user
from schemas.user import User, UserCreate

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post(
    "/user",
    response_model=User
)
async def register_user(user: UserCreate, db: Session = Depends(get_db)) -> User:
    """Register a new user."""
    existing_user = get_user_by_username(user.username, db)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists"
        )

    existing_email = get_user_by_email(user.email, db)
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists."
        )

    return create_user(user, db)
