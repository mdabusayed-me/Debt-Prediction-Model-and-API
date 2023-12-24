from fastapi import APIRouter
from modules.loan.loan import router as loan_router
from modules.dropdownInfo.dropdownInfo import router as dropdownInfo_router

api_router = APIRouter()

api_router.include_router(loan_router, prefix="/loan", tags=["Loan Info"])
api_router.include_router(dropdownInfo_router, prefix="/dropdownInfo", tags=["Dropdown Info"])
