from fastapi import FastAPI, HTTPException
import mysql.connector
import uvicorn
import numpy as np 
import pickle
import pandas as pd
import requests

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="debt_db2"
)


app = FastAPI()

@app.get("/")
def index():
    return{"hellow": "FastAPI"}

# Get all loan_data
@app.get("/loan_data")
def get_loan_data():
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM loan_data")
    result = cursor.fetchall()
    return {"loan_data": result}

# Add a new loan data
@app.post("/loan_data")
def add_loan_data(Gender: str, Married: str, Dependents: int, Education: str, Self_Employed: str, ApplicantIncome: int, CoapplicantIncome: int, LoanAmount: int, Loan_Amount_Term: int, Credit_History: int,  Property_Area: str, Loan_Status: str):
    cursor = mydb.cursor()
    sql = "INSERT INTO loan_data (Gender, Married, Dependents, Education, Self_Employed, ApplicantIncome, CoapplicantIncome, LoanAmount, Loan_Amount_Term, Credit_History, Property_Area, Loan_Status) VALUES (%s, %s, %s ,%s, %s ,%s, %s ,%s, %s ,%s, %s, %s)"
    val = (Gender, Married, Dependents, Education, Self_Employed, ApplicantIncome, CoapplicantIncome, LoanAmount, Loan_Amount_Term, Credit_History, Property_Area, Loan_Status)
    cursor.execute(sql, val)
    mydb.commit()
    return {"message": "Loan_data added successfully"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

