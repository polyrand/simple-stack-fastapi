"""Dependecy injection."""


from typing import Generator
import secrets

# from sqlalchemy.orm import Session

# from app import crud, models, schemas
from app import db
from app import crud
from app import schemas
from app.core import security
from app.core.config import settings

# from app.db.session import SessionLocal
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials, OAuth2PasswordBearerm
from jose import jwt
from pydantic import ValidationError

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)

httpauth = HTTPBasic()


def authorize(credentials: HTTPBasicCredentials = Depends(httpauth)) -> bool:
    correct_username = secrets.compare_digest(
        credentials.username, settings.API_USERNAME
    )
    correct_password = secrets.compare_digest(
        credentials.password, settings.API_PASSWORD
    )
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return True


async def get_current_user(token: str = Depends(reusable_oauth2)) -> schemas.User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = schemas.TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )

    user = await crud.user_get(id=token_data.sub)
    # user = crud.user.get(db, id=token_data.sub)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


async def get_user_level(
    current_user: schemas.User = Depends(get_current_user),
) -> schemas.User:
    user_level = await crud.get_user_level()
    return user_level


# def get_current_active_user(
#     current_user: models.User = Depends(get_current_user),
# ) -> models.User:
#     if not crud.user.is_active(current_user):
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user


# def get_current_active_superuser(
#     current_user: models.User = Depends(get_current_user),
# ) -> models.User:
#     if not crud.user.is_superuser(current_user):
#         raise HTTPException(
#             status_code=400, detail="The user doesn't have enough privileges"
#         )
#     return current_user

# def get_db() -> Generator:
#     try:
#         db = SessionLocal()
#         yield db
#     finally:
#         db.close()
