from pydantic import BaseModel

class CreateUser(BaseModel):
    username: str
    login: str
    email: str
    age: int
    password: str

class UpdateUser(BaseModel):
    username: str
    age: int
    password: str

class CreateGame(BaseModel):
    title: str
    description: str
    cost: float
    description: float
    size: float

class UpdateGame(BaseModel):
    title: str
    description: str
    cost: float
    description: float
    size: float