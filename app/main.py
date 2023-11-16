import time

import psycopg2
from fastapi import FastAPI, Response, status, HTTPException
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel


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


@app.get('/posts')
def get_posts():
    cursor.execute('''SELECT * FROM posts ''')
    posts = cursor.fetchall()
    return {'data': posts}


@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute(f'INSERT INTO posts (title, content, published) VALUES({post.title}, {post.content})')
    cursor.execute('''INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) ''',
                   (post.title, post.content, post.published))
    return {'data': 'created post'}


@app.get('/posts/{id}')
def get_post(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id: {id} was not found')
    return {'post detail': post}


@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id: {id} does not exist')

    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put('/posts/{id}')
def update_post(id: int, post: Post):
    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id: {id} does not exist')
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {'data': post_dict}
