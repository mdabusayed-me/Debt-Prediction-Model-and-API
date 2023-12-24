from fastapi import FastAPI
from modules.router import api_router

app = FastAPI()

@app.get("/")
def index():
    return{"hello": "FastAPI is working"}

app.include_router(api_router, prefix='')
