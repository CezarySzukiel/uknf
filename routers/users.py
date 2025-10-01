from fastapi import APIRouter, Depends

from schemas.user import User

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get("/")
def get_if_user_exists(user) -> User | None:
    if user:
        return User.model_validate(user)
    return None
