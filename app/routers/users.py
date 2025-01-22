from fastapi import APIRouter, Depends, status, HTTPException, Request
from sqlalchemy.orm import Session
from backend.db import get_db
from typing import Annotated
from models import User, Game
from shemas import CreateUser, UpdateUser
from sqlalchemy import insert, select, update, delete
from slugify import slugify
from fastapi.responses import HTMLResponse

from fastapi.templating import Jinja2Templates
from utils import get_password_hash


router = APIRouter(prefix='/user', tags=['user'])

templates = Jinja2Templates(directory='templates')


@router.post("/register/", response_class=HTMLResponse)
async def register_user(request: Request, username: str, email: str, password: str, age: int, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Пользователь уже существует")

    hashed_password = get_password_hash(password)
    new_user = User(username=username, email=email, hashed_password=hashed_password, age=age, slug=slugify(username))

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return templates.TemplateResponse('users.html', {'request': request})



@router.get('/all_users')
async def all_user(db: Annotated[Session, Depends(get_db)]):
    users = db.scalars(select(User)).all()
    return users

@router.get('/user_id')
async def user_by_id(db: Annotated[Session, Depends(get_db)], user_id: int):
    user = db.scalars(select(User).where(User.id == user_id))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User was not found'
        )
    else:
        return user

@router.post('/create')
async def create_user(db: Annotated[Session, Depends(get_db)], create_user: CreateUser):
    db.execute(insert(User).values(username=create_user.username,
                                   email=create_user.email,
                                   age=create_user.age,
                                   hashed_password=get_password_hash(create_user.password),
                                   slug=slugify(create_user.username)))
    db.commit()
    return {'status_code': status.HTTP_201_CREATED,
            'transaction': 'Successful'}

@router.put('/update')
async def update_user(db: Annotated[Session, Depends(get_db)], user_id: int, update_user: UpdateUser):
    user = db.scalars(select(User).where(User.id == user_id))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User was not found'
        )

    db.execute(update(User).where(User.id == user_id).values(
        username=update_user.username,
        hashed_password=get_password_hash(create_user.password),
        age=update_user.age))

    db.commit()

    return {'status_code': status.HTTP_200_OK,
         'transaction': 'User update is successful!'}


@router.delete('/delete')
async def delete_user(db: Annotated[Session, Depends(get_db)], user_id: int):
    user = db.scalars(select(User).where(User.id == user_id))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User was not found'
        )
    db.execute(delete(User).where(User.id == user_id))
    db.commit()

    return {'status_code': status.HTTP_200_OK,
         'transaction': 'User delete is successful!'}