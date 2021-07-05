from db import *
from enum import Enum
from authentication import *
from typing import Optional
from pydantic import BaseModel
from fastapi import APIRouter, Header, HTTPException
from fastapi.responses import JSONResponse

class Business(BaseModel):
    name: str
    date: str
    lat: float
    lng: float
    description: str
    ownerid: int

router = APIRouter(prefix='/businesses', responses={404: {'description': 'Not Found'}})

# return all users
@router.get('/')
def all_businesses():
    query = 'SELECT * FROM foodtrucks;'
    result = query_no_data(query, cursor, cnx)
    return result

# return a specific business by id
@router.get('/business')
def get_business(id: int):
    query = 'SELECT * FROM foodtrucks WHERE id=%s;'
    data = (id, )
    result = query_return(query, data, cursor, cnx)
    return result

# return a business id by username
@router.get('/id')
def get_business_by_name(name: str):
    query = 'SELECT business_id FROM users WHERE username=%s;'
    data = (name, )
    result = query_return(query, data, cursor, cnx)
    return result

# create new business 
@router.post('/new', status_code=201)
async def new_business(business: Business):
    query = 'INSERT INTO foodtrucks (name, date, lat, lng, description, ownerid) VALUES (%s, %s, %s, %s, %s, %s);'
    data = (business.name, business.date, business.lat, business.lng, business.description, business.ownerid)
    query_(query, data, cursor, cnx)
    return 'Business created: {0}'.format(data)

# update business name 
@router.patch('/update_name', status_code=200)
def update_business_name(id: int, name: str):
    query = 'UPDATE foodtrucks SET name=%s WHERE id=%s;'
    data = (name, id)
    query_(query, data, cursor, cnx)
    return 'Updated business name to {0} with id {1}'.format(name, id)

# update business description 
@router.patch('/update_description', status_code=200)
def update_business_description(id: int, description: str):
    query = 'UPDATE foodtrucks SET description=%s WHERE id=%s;'
    data = (description, id)
    query_(query, data, cursor, cnx)
    return 'Updated business description to {0} with id {1}'.format(description, id)

# update business date
@router.patch('/update_date', status_code=200)
def update_business_date(id: int, date: str):
    query = 'UPDATE foodtrucks SET date=%s WHERE id=%s;'
    data = (date, id)
    query_(query, data, cursor, cnx)
    return 'Updated location date to {0} with business id {1}'.format(date, id)

# update business location
@router.patch('/update_location', status_code=200)
def update_business_location(id: int, lat: float, lng: float):
    query = 'UPDATE foodtrucks SET lat=%s, lng=%s WHERE id=%s;'
    data = (lat, lng, id)
    query_(query, data, cursor, cnx)
    return 'Updated location to lat {0} lng {1} with business id {2}'.format(lat, lng, id)

# delete business by id
@router.delete('/delete', status_code=200)
def delete_business(id: int):
    query = 'DELETE FROM foodtrucks WHERE id=%s;'
    data = (id, )
    query_(query, data, cursor, cnx)
    return 'Account deleted with id {0}'.format(id)
