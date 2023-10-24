#https://www.youtube.com/watch?v=0sOvCWFmrtA&t=28139s

from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
@app.get("/")
def root():
    return {"message": "Welcome to my new API"}

#run the command below into the terminal to rerun the website
#uvicorn main:app --reload --port 8001

@app.get("/posts")
def get_posts():
    return {"data": "This is your post"}

@app.post("/createposts")
def create_posts(new_post: Post):
    print(new_post.title)
    return {"data": "new post"}




