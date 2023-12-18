from fastapi import FastAPI
import uvicorn
import numpy as np 
import pickle
import pandas as pd


app = FastAPI()

@app.get("/")
def index():
    return{"hellow": "FastAPI"}





if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

