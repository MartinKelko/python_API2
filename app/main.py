import time

import psycopg2
from fastapi import FastAPI, Response, status, HTTPException, Depends
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel
from sqlalchemy.orm import Session
from . import models
from .database import engine, get_db

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

class Post(BaseModel):
    title: str
    content: str
    published: bool = True


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


@app.get('/')
def root():
    return {'message': 'Welcome to my new API. This is welcome screen!'}

@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):

    posts = db.query(models.Post).all()

    print(posts)
    return {"data": "successfull"}

@app.get('/posts')
def get_posts(db: Session = Depends(get_db)):
    cursor.execute('''SELECT * FROM posts ''')
    posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return {'data': posts}


@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute('''INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * ''',
                   (post.title, post.content, post.published))
    new_post = cursor.fetchone()

    conn.commit()

    return {'data': new_post}


@app.get('/posts/{id}')
def get_post(id: str):
    cursor.execute("""SELECT * from posts WHERE id = %s """, (str(id),))
    post = cursor.fetchone()
    if not post:
    print(test_post)
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id: {id} was not found')
    return {'post detail': post}


@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):

    cursor.execute("""DELETE FROM posts WHERE id = %s returning *""", (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()

    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id: {id} does not exist')

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put('/posts/{id}')
def update_post(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s 
    RETURNING *""",
                   (post.title, post.content, post.published, str(id)))

    updated_post = cursor.fetchone()
    conn.commit()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id: {id} does not exist')

    return {'data': updated_post}
