from fastapi import APIRouter, Depends, status, HTTPException, Request
from sqlalchemy.orm import Session
from backend.db import get_db
from typing import Annotated
from models import User, Game
from shemas import CreateUser, UpdateUser, UpdateGame, CreateGame
from sqlalchemy import insert, select, update, delete
from slugify import slugify
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix='/game', tags=['game'])
templates = Jinja2Templates(directory='templates')

@router.post('/')
async def home(request: Request, db: Annotated[Session, Depends(get_db)]) -> HTMLResponse:
    game = db.scalars(select(Game)).all()
    return templates.TemplateResponse('games.html', {'request': request, 'games': game})

@router.get('/all_game')
async def all_game(db: Annotated[Session, Depends(get_db)]):
    game = db.scalars(select(Game)).all()
    return game

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
async def create_game(db: Annotated[Session, Depends(get_db)], create_game: CreateGame):
    db.execute(insert(Game).values(title=create_game.title,
                                   description=create_game.description,
                                   age_limited=create_game.age_limited,
                                   size=create_game.size,
                                   cost=create_game.cost,
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
async def delete_game(db: Annotated[Session, Depends(get_db)], game_id: int):
    task = db.scalars(select(Game).where(Game.id == game_id))
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Games was not found'
        )
    db.execute(delete(Game).where(Game.id == game_id))
    db.commit()

    return {'status_code': status.HTTP_200_OK,
         'transaction': 'Games delete is successful!'}
