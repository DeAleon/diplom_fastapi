from fastapi import FastAPI
from routers import games, users

app = FastAPI()

@app.get('/')
async def welcome() -> dict:
    return {"message": "Welcome to Taskmanager"}


app.include_router(games.router)
app.include_router(users.router)