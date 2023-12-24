from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import mysql.connector
import numpy as np
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse 
import pickle            
import joblib
import pandas as pd
from fastapi import Request, status
import json





mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="debt_db2"
)

# df = pd.read_csv('E:\Debt Prediction Model and API\\files\csv\loan_data.csv')

app = FastAPI()


@app.get("/")
def index():
    return{"hellow": "FastAPI"}

# @app.get("/getalldata")
# def getalldata():
#     df = pd.read_csv('E:\Debt Prediction Model and API\nfiles\csv\loan_data.csv').T.to_dict()
#     return df


# Get all loan_data
@app.get("/get_loan_data")
def get_loan_data():
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM loan_data")
    result = cursor.fetchall()
    return {"loan_data": result}

# Add a new loan data
@app.post("/loan_data")
def add_loan_data(Loan_ID: str, Gender: str, Married: str, Dependents: int, Education: str, Self_Employed: str, ApplicantIncome: int, CoapplicantIncome: int, LoanAmount: int, Loan_Amount_Term: int, Credit_History: int,  Property_Area: str, Loan_Status: str):
    cursor = mydb.cursor()
    sql = "INSERT INTO loan_data (Loan_ID, Gender, Married, Dependents, Education, Self_Employed, ApplicantIncome, CoapplicantIncome, LoanAmount, Loan_Amount_Term, Credit_History, Property_Area, Loan_Status) VALUES (%s, %s, %s, %s ,%s, %s ,%s, %s ,%s, %s ,%s, %s, %s)"
    val = (Loan_ID, Gender, Married, Dependents, Education, Self_Employed, ApplicantIncome, CoapplicantIncome, LoanAmount, Loan_Amount_Term, Credit_History, Property_Area, Loan_Status)
    result = cursor.execute(sql, val)
    mydb.commit()
    return {"Posted Data": result}

@app.get("/loan_data_Gender")
async def get_loan_data():
    cursor = mydb.cursor()
    cursor.execute("SELECT Gender FROM loan_data")
    result = cursor.fetchone()
    if result is None:
        raise HTTPException(status_code=404, detail="not found")
    return {"Property_Area": result}
    # return {"loan_data": result}

@app.get("/loan_data_Property_Area")
async def get_loan_data():
    cursor = mydb.cursor()
    cursor.execute("SELECT Property_Area FROM loan_data")
    result = cursor.fetchone()
    if result is None:
        raise HTTPException(status_code=404, detail="not found")
    return {"Property_Area": result}
    # return {"loan_data": result}


# Add a new loan data
@app.post("/loan_data_Dependents")
def add_loan_data(Dependents: int):
    cursor = mydb.cursor()
    sql = "INSERT INTO loan_data (Dependents) VALUES (%s)"
    val = (Dependents)
    result = cursor.execute(sql, val)
    mydb.commit()
    return {"Posted Data": result}



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

