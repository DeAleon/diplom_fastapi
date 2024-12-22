from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from backend.db import get_db
from typing import Annotated
from models import User, Game
from shemas import CreateUser, UpdateUser, UpdateGame, CreateGame
from sqlalchemy import insert, select, update, delete
from slugify import slugify


router = APIRouter(prefix='/game', tags=['game'])


@router.get('/')
async def all_game(db: Annotated[Session, Depends(get_db)]):
    task = db.scalars(select(Game)).all()
    return task

@router.get('/game_id')
async def game_by_id(db: Annotated[Session, Depends(get_db)], game_id: int):
    game = db.scalars(select(Game).where(Game.id == game_id))
    if game is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User was not found'
        )
    else:
        return game

@router.post('/create')
async def create_game(db: Annotated[Session, Depends(get_db)], create_game: CreateGame, users_id: int):
    db.execute(insert(Game).values(title=create_game.title,
                                   description=create_game.description,
                                   cost=create_game.cost,
                                   user_id=users_id,
                                   slug=slugify(create_game.title)))
    db.commit()
    return {'status_code': status.HTTP_201_CREATED,
            'transaction': 'Successful'}

@router.put('/update')
async def update_game(db: Annotated[Session, Depends(get_db)], game_id: int, update_game: UpdateGame):
    game = db.scalars(select(Game).where(Game.id == game_id))
    if game is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Games was not found'
        )

    db.execute(update(Game).where(Game.id == game_id).values(
        title=create_game.title,
        content=create_game.content,
        priority=create_game.priority))

    db.commit()

    return {'status_code': status.HTTP_200_OK,
         'transaction': 'Games update is successful!'}

@router.delete('/delete')
async def delete_game(db: Annotated[Session, Depends(get_db)], task_id: int):
    task = db.scalars(select(Game).where(Game.id == task_id))
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Games was not found'
        )
    db.execute(delete(Game).where(Game.id == task_id))
    db.commit()

    return {'status_code': status.HTTP_200_OK,
         'transaction': 'Games delete is successful!'}
