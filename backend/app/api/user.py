from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from app.db.session import get_db
from app.db.crud import CRUDBase
from app.schemas.user import LoginRequest, UserCreate, UserCreate, UserUpdate
from app.utils.security import create_access_token, get_password_hash
from app.services.user import authenticate, get_current_active_user, get_user_role
from app.models.users import Users

import logging
logger = logging.getLogger(__name__)


user_router = APIRouter()
user_crud = CRUDBase(model=Users)

@user_router.post("/login", tags=["auth"])
def login(user_data: LoginRequest = Depends(), db: Session = Depends(get_db)):
    try:
        user_data.model_dump()
        user_auth = authenticate(db, username=user_data.username, password=user_data.password)
        if not user_auth:
            raise HTTPException(status_code=400, detail="Incorrect username or password")
        elif user_auth.user_type != user_data.user_type:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User Type Missmatch")
        content = {
            "message": "Login Sucessful",
            "user_type": user_data.user_type
        }
        response = JSONResponse(content=content)
        access_token = create_access_token(user_auth.username)
        response.set_cookie(key="Authorization", value=access_token, samesite='lax', secure=False)
        return response
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))


@user_router.post("/logout", tags=['auth'])
def logout():
    try:
        content = {
            "message": "Logout Successful"
        }
        response = JSONResponse(content=content)
        response.delete_cookie(key="Authorization")
        return response
    except Exception as e:
        logger.error(e)


@user_router.get("/users/me", tags=["user"])
def get_user(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user),
):
    try:
        response_data = {
            # "id": current_user.id,
            "email": current_user.email,
            "username": current_user.username
        }
        return JSONResponse(status_code=status.HTTP_200_OK, content=response_data)

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not Found")



@user_router.get("/users/all", tags={"user"})
def get_all_user(
    db:Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    try:
        users = db.query(Users).all()
        response_data = []
        for user in users:
            return_user = {
                "email": user.email,
                "username": user.username
            }
            response_data.append(return_user)
        return JSONResponse(status_code=status.HTTP_200_OK, content=response_data)
    except Exception as e:
        logger.error(e) 


@user_router.post("/users", status_code=201, tags=["user"])
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        user.model_dump()
        exist_user = db.query(Users).filter(Users.username == user.username).first()
        if exist_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username Already Exist")
        user.password = get_password_hash(user.password)
        user = user_crud.create(db=db, obj_in=user)
        response_data = {
            # "id": user.id,
            "email": user.email,
            "username": user.username,
            "user_type": user.user_type
        }
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=response_data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))


@user_router.put("/users", tags=["user"])
def update_user(
    upd_user: UserUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user),
):
    if not current_user:
        raise HTTPException(status_code=400, detail="No user found")
    current_user.username = upd_user.username
    current_user.email = upd_user.email
    current_user.password = get_password_hash(upd_user.password)
    current_user.user_type = upd_user.user_type
    return user_crud.update(db, obj_in=current_user)


@user_router.delete("/users/{username}", tags=["user"])
def delete_user(
    username:str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    try:
        if current_user.user_type in ["admin"]:
            user = db.query(Users).filter(Users.username == username).first()
            if user:
                db.delete(user)
                db.commit()
            else:
                return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content="User not found")
            return JSONResponse(status_code=status.HTTP_200_OK, content="User Deleted")
        else:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content="Resource not allowed")
    except Exception as e:
        logger.error(e)
