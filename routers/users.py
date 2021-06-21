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

class Card(BaseModel):
    cardname: str
    cc: str
    ccdate: str
    cvv: int

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

# add card to account
@router.patch('/add_card', status_code=200)
def add_card_to_acc(id: int, card: Card):
    query = 'UPDATE users SET cardname=%s, cc=%s, ccdate=%s, cvv=%s WHERE id=%s;'
    data = (card.cardname, card.cc, card.ccdate, card.cvv, id)
    query_(query, data, cursor, cnx)
    return 'Card number added to account with id {0}'.format(id)

# delete user by id
@router.delete('/delete_user', status_code=200)
def delete_user(id: int):
    query = 'DELETE FROM users WHERE id=%s;'
    data = (id, )
    query_(query, data, cursor, cnx)
    return 'Account deleted with id {0}'.format(id)