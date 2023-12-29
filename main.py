from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from modules.router import api_router

# import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/")
def index():
    return{"hello": "FastAPI is working"}

app.include_router(api_router, prefix='')

# if __name__ == "__main__":
#     uvicorn.run("main:app", reload=True, port=8000, host="0.0.0.0")
