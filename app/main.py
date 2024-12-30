from fastapi import FastAPI, Path, HTTPException, Request, Form
from routers import games, users
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory='templates')

@app.get('/')
async def welcome(request: Request) -> HTMLResponse:
    return templates.TemplateResponse('main.html', {'request': request})


app.include_router(games.router)
app.include_router(users.router)