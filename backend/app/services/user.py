from jose import JWTError, jwt
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Depends, Header, Cookie
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime
from typing import Optional,Union, Any

from app.db.session import get_db
from app.models.users import Users
from config.config import settings
from config.logging import logger
from app.schemas.user import TokenData, TokenPayload
from app.db.crud import CRUDBase
import logging

from app.utils.security import verify_password


logger = logging.getLogger(__name__)
user_crud = CRUDBase(model=Users)

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials"
)


def authenticate(db: Session, *, username: Optional[str] = None, password: str):
    user = user_crud.get_by_field(db, field="username", value=username)

    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user


def get_token_bearer(token: str = Header(...)):
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError as e:
        logger.error(f"error {e}")
        raise credentials_exception
    return token_data



def get_token(token:str = Cookie(None, alias="Authorization")):
    if token is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden, Token is required")
    return token

def get_current_active_user(token: str = Depends(get_token), db: Session = Depends(get_db)):
    try:
        if token is None:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Token Missing")
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail="Token expired"
            )
        user: Union[dict[str, Any], None] = user_crud.get_by_field(db, field="username", value=token_data.sub)
        if user is None:
            raise credentials_exception
        return user
    except Exception as e:
        logger.error(f"error {e}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User Not Authenticated")

def get_user_role(user):
    user = user_crud.get_by_field(db, field="username", value=username).first()
    return user.user_type