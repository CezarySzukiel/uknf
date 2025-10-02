from datetime import timedelta

from fastapi import APIRouter, HTTPException, status, Depends, Cookie
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from core.config import settings
from core.security import create_access_token, create_refresh_token, verify_refresh_token
from core.database import get_db
from crud.auth import authenticate_user
from crud.user import get_user_by_username
from schemas.token import Token, TokenPair

router = APIRouter(
    tags=["authentication"],
)


# @router.post(
#     "/token",
#     response_model=Token
# )
# async def login_for_access_token(
#         form_data: OAuth2PasswordRequestForm = Depends(),
#         db: Session = Depends(get_db)
# ):
#     user = authenticate_user(form_data.username, form_data.password, db)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#         )
#
#     access_token = create_access_token(data={"name": user.username})
#
#     return {"access_token": access_token, "token_type": "bearer"}

@router.post("/token", response_model=TokenPair)
async def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)
):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )

    access_token = create_access_token(data={"sub": user.username})
    refresh_token = create_refresh_token(data={"sub": user.username})

    response = JSONResponse(
        content={"access_token": access_token, "token_type": "bearer"}
    )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,  # tylko przez HTTPS
        samesite="strict"
    )

    return response


@router.post("/refresh", response_model=Token)
async def refresh_access_token(
        refresh_token: str = Cookie(None),
        db: Session = Depends(get_db)
):
    if not refresh_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token missing")

    payload = verify_refresh_token(refresh_token)
    username = payload.get("sub")

    user = get_user_by_username(username, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    verify_refresh_token(refresh_token)

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    new_access_token = create_access_token(
        data={"sub": user.username, "type": "access"},
        expires_delta=access_token_expires
    )

    return {"access_token": new_access_token, "token_type": "bearer"}
