from fastapi import APIRouter
from os import environ as env
from typing import List
from pydantic import BaseModel
import db_connection


router = APIRouter()

class DropdownResponse(BaseModel):
    data: List[str]


con, cur, db = db_connection.get_db()

@router.post("/add_loan_train_data")
async def add_loan(Gender: str, Married: str, Dependents: int, Education: str, Self_Employed: str, ApplicantIncome: float, CoapplicantIncome: float, LoanAmount: float, Loan_Amount_Term: int, Credit_History: float, Property_Area: str, Loan_Status: str):
    cursor = con.cursor()
    query = "INSERT INTO loans (Gender, Married, Dependents, Education, Self_Employed, ApplicantIncome, CoapplicantIncome, LoanAmount, Loan_Amount_Term, Credit_History, Property_Area, Loan_Status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    values = (Gender, Married, Dependents, Education, Self_Employed, ApplicantIncome, CoapplicantIncome, LoanAmount, Loan_Amount_Term, Credit_History, Property_Area, Loan_Status)
    cursor.execute(query, values)
    con.commit()
    cursor.close()
    return {"message": "Loan added successfully"}


@router.get("/loan_train_data")
async def get_loan_train_data():
    cursor = con.cursor()
    query = "SELECT * FROM loan_train_data"
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()

    # Convert data to object with column names as key-value pairs
    columns = [desc[0] for desc in cursor.description]
    result = []
    for row in data:
        result.append(dict(zip(columns, row)))

    return {"data": result}
