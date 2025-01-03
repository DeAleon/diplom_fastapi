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


router = APIRouter(prefix='/user', tags=['user'])
templates = Jinja2Templates(directory='templates')

@router.post('/')
async def register_user(request: Request, db: Annotated[Session, Depends(get_db)],
                        create_user: CreateUser) -> HTMLResponse:
    reg = db.execute(insert(User).values(username=create_user.username,
                                   login=create_user.login,
                                   email=create_user.email,
                                   age=create_user.age,
                                   password=create_user.password,
                                   slug=slugify(create_user.username)))
    db.commit()
    return templates.TemplateResponse('games.html', {'request': request, 'reg': reg})

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
                                   login=create_user.login,
                                   email=create_user.email,
                                   age=create_user.age,
                                   password=create_user.password,
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
        password=update_user.password,
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