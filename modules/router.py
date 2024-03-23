from fastapi import APIRouter
# from modules.loan.loan import router as loan_router
# from modules.dropdownInfo.dropdownInfo import router as dropdownInfo_router
# from modules.prediction.prediction import router as prediction_router
from modules.faq.faq import router as faq_router

api_router = APIRouter()

# api_router.include_router(loan_router, prefix="/loan", tags=["Loan Info"])
# api_router.include_router(dropdownInfo_router, prefix="/dropdownInfo", tags=["Dropdown Info"])
# api_router.include_router(prediction_router, prefix="/prediction", tags=["Prediction"])
api_router.include_router(faq_router, prefix="/faq", tags=["FAQ"])
