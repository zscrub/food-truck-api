from db import *
from enum import Enum
from authentication import *
from typing import Optional
from pydantic import BaseModel
from fastapi import APIRouter, Header, HTTPException
from fastapi.responses import JSONResponse

class User(BaseModel):
    username: str
    password: str
    email: str
    cardname: None
    cc: None
    ccdate: None
    cvv: None

router = APIRouter(prefix='/users', responses={404: {'description':'Not Found'}})

# return all users
@router.get('/')
def all_users():
    query = 'SELECT * FROM users;'
    result = query_no_data(query, cursor, cnx)
    return result

# return a specific user
@router.get('/user')
def get_user(id: int):
    query = 'SELECT * FROM users WHERE id=%s;'
    data = (id, )
    result = query_return(query, data, cursor, cnx)
    return result

# create new user
@router.post('/new', status_code=201)
async def new_user(user: User):
    query = 'INSERT INTO users (username, password, email) VALUES (%s, %s, %s);'
    data = (user.username, user.password, user.email)
    query_(query, data, cursor, cnx)
    return 'User created: {0}'.format(data)

@router.patch('/add_card', status_code=200)
def add_card_to_acc(id: int, cardname: str, cc: str, ccdate: str, cvv: int):
    query = 'UPDATE users SET (cardname=%s, cc=%s, ccdate=%s, cvv=%d) WHERE id=%d;'
    data = (cardname, cc, ccdate, cvv, id)
    query_(query, data, cursor, cnx)