from fastapi import (APIRouter, Body, Depends, File, HTTPException, Query,
                     Request, UploadFile)
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_hello_world():
    return {"message": "Hello, World!"}
