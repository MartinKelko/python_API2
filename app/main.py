import time
from typing import Optional, List
import psycopg2
from fastapi import FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from psycopg2.extras import RealDictCursor
from . import models, schemas, utils
from .database import engine, get_db
from .routers import post, user, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

hidden_imports = [
    'uvicorn.logging',
    'uvicorn.loops',
    'uvicorn.loops.auto',
    'uvicorn.protocols',
    'uvicorn.protocols.http',
    'uvicorn.protocols.http.auto',
    'uvicorn.protocols.websockets',
    'uvicorn.protocols.websockets.auto',
    'uvicorn.lifespan',
    'uvicorn.lifespan.on',
    'app',
]

# Database access constants
HOST = 'localhost'
DATABASE = 'fastapi'
USER = 'admin'
PASSWORD = '0000'

while True:
    try:
        conn = psycopg2.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD, cursor_factory=RealDictCursor)
        # conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='Nepijemrum22_22', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('Database connection was successful!')
        break
    except Exception as error:
        print('Connecting to database failed!')
        print('Error: ', error)
        time.sleep(3)

my_posts = [{'title': 'title of post 1', 'content': 'content of post 1', 'id': 1},
            {'title': 'favorite foods', 'content': 'I like pizza', 'id': 2}]


def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p


def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get('/')
def root():
    return {'message': 'Welcome to my new API. This is welcome screen!'}





