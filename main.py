from db import *
from pydantic import BaseModel
from fastapi import Depends, FastAPI

app = FastAPI()

@app.get('/')
def home():
    return "Food-Trucks-API"