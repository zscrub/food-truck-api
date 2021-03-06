# “On my honor, I have neither received nor given any unauthorized assistance on this assignment.” Zachary Rubin

from db import *
from pydantic import BaseModel
from fastapi import Depends, FastAPI
from routers import users, foodtrucks

app = FastAPI()
app.include_router(users.router)
app.include_router(foodtrucks.router)

@app.get('/')
def home():
    return 'Food-Trucks-API'

if __name__ == "__main__":
    app.run(debug=True)