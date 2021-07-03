
from db import *
from bcrypt import *
from enum import Enum
from authentication import *
from typing import Optional
from datetime import timedelta
from pydantic import BaseModel, main
from passlib.hash import sha256_crypt
from fastapi_login import LoginManager
from fastapi_login import LoginManager
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Header, HTTPException, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi_login.exceptions import InvalidCredentialsException

class User(BaseModel):
    username: str
    password: str
    email: str
    account_type: str

    def __repr__(self):
        return 'User {0}'.format(self.id)

class Login(BaseModel):
    username: str
    email: str
    password: str

class Card(BaseModel):
    cardname: str
    cc: str
    ccdate: str
    cvv: str

salt = gensalt()

manager = LoginManager(secret_key, token_url='/auth/token')

router = APIRouter(prefix='/users', responses={404: {'description':'Not Found'}})

# return all users
@router.get('/')
def all_users():
    query = 'SELECT * FROM users;'
    result = query_no_data(query, cursor, cnx)
    return result

# def all_users(auth: Optional[str] = Header(None)):
#     auth_ = check_auth(auth)
#     if auth_ == False:
#         raise HTTPException(status_code=403, detail='Login')

#     ac = path_handler(auth_['role'], ('p', 'a'))
#     match ac:
#         case True:    
#             query = 'SELECT * FROM users;'
#             result = query_no_data(query, cursor, cnx)
#             return result
#         case False:
#             return 401
#         case _:
#             raise HTTPException(status_code=403, detail='Login')

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
    username = user.username
    username = ''.join(e for e in username if e.isalnum())
    email = user.email
    email = ''.join(e for e in email if e.isalnum() or e == '@' or e == '.')
    password = hashpw(user.password.encode(), salt)
    query = 'INSERT INTO users (username, password, email, account_type) VALUES (%s, %s, %s, %s);'
    data = (username, password, email, user.account_type)
    query_(query, data, cursor, cnx)
    return 'User created: {0}'.format(data)

# add card to account
@router.patch('/add_card', status_code=200)
def add_card_to_acc(id: int, card: Card):
    query = 'UPDATE users SET cardname=%s, cc=%s, ccdate=%s, cvv=%s WHERE id=%s;'
    data = (card.cardname, sha256_crypt.encrypt(card.cc), sha256_crypt.encrypt(card.ccdate), sha256_crypt.encrypt(str(card.cvv)), id)
    query_(query, data, cursor, cnx)
    return 'Card number added to account with id {0}'.format(id)

# update account type
@router.patch('/update_account_type', status_code=200)
def update_account_type(id: int, account_type: str):
    query = 'UPDATE users SET account_type=%s WHERE id=%s;'
    data = (account_type, id)
    query_(query, data, cursor, cnx)
    return 'Updated account_type to {0} with id {1}'.format(account_type, id)

# delete user by id
@router.delete('/delete', status_code=200)
def delete_user(id: int):
    query = 'DELETE FROM users WHERE id=%s;'
    data = (id, )
    query_(query, data, cursor, cnx)
    return 'Account deleted with id {0}'.format(id)

# log in/OAuth2

@manager.user_loader
def load_user(username: str):
    query = 'SELECT * FROM users WHERE username=%s;'
    data = (username, )
    user = query_return(query, data, cursor, cnx)
    return user

@router.post('/auth/token')
def login(data: OAuth2PasswordRequestForm = Depends()):
    username = data.username
    password = data.password

    user = load_user(username)

    if not user:
        raise InvalidCredentialsException
    elif not checkpw(password.encode(), user[0]['password'].encode()):
        raise InvalidCredentialsException

    access_token = manager.create_access_token(
        data = dict(sub=username),
        expires = timedelta(hours=12)
    )
    return {'access_token': access_token, 'token_type': 'bearer'}