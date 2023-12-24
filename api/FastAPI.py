import _mysql_connector
from fastapi import FastAPI, HTTPException, requests
import mysql.connector
import uvicorn
import numpy as np 
import pickle
import joblib
import pandas as pd
import traceback
from sqlalchemy import create_engine, Column, String, MetaData, Table


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
    cursor.execute(sql, val)
    mydb.commit()
    return {"message": "Loan_data added successfully"}


@app.get("/loan_data_aandg")
def get_loan_data():
    cursor = mydb.cursor()
    cursor.execute("SELECT Property_Area, Gender FROM loan_data")
    result = cursor.fetchone()
    if result is None:
        raise HTTPException(status_code=404, detail="not found")
    return {"Property_Area": result[0], "Gender": result[1]}
    # return {"loan_data": result}


host = "sql12.freesqldatabase.com"
database_name = "sql12671479"
user = "sql12671479"
password = "jcVXxlPEcP"
port = 3306

DATABASE_URL = f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database_name}"
engine = create_engine(DATABASE_URL)

metadata = MetaData()
app = FastAPI()

The_Table = Table(
    "TABLE 1",
    metadata,
    Column("Dependents", String),
    Column("Married", String),
    Column("Education", String),
    Column("Self_Employed", String)

)

@app.get("/distinct-values/{column_name}")
async def get_distinct_values(column_name: str):
    try:
        # Dynamically retrieve the list of column names
        table_columns = [column.name for column in The_Table.columns]

        # Check if the specified column is in the list of available columns
        if column_name not in table_columns:
            raise HTTPException(status_code=404, detail=f"Column '{column_name}' not found in the table.")
        
        with engine.connect() as connection:
            # Construct the query dynamically
            query = select(distinct(The_Table.c[column_name]))
            
            # Execute the query
            result = connection.execute(query)
            
            # Fetch distinct values from the result
            distinct_values = [row[0] for row in result]

        return {"distinct_values": distinct_values}
    except HTTPException as http_exc:
        raise http_exc  # Re-raise the HTTPException with the correct status code
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        traceback.print_exc()  # Print the traceback information
        raise HTTPException(status_code=500, detail="Internal Server Error")
