#https://www.youtube.com/watch?v=0sOvCWFmrtA&t=28139s

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Ahoj222"}

#run below command into the terminal to rerun the website
#uvicorn main:app --reload --port 8001
