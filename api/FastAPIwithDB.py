from fastapi import FastAPI, HTTPException, Depends, UploadFile, File, Query
from fastapi.responses import JSONResponse
from fastapi.openapi.models import Response
import csv
import mysql.connector
from mysql.connector import errorcode

app = FastAPI()

# MySQL Database Configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'loan_db',
}

def create_table():
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Define the table schema
        table_schema = (
            "CREATE TABLE IF NOT EXISTS loan_data ("
            "Loan_ID VARCHAR(255) PRIMARY KEY,"
            "Gender VARCHAR(255),"
            "Married VARCHAR(255),"
            "Dependents VARCHAR(255),"
            "Education VARCHAR(255),"
            "Self_Employed VARCHAR(255),"
            "ApplicantIncome INT,"
            "CoapplicantIncome INT,"
            "LoanAmount INT,"
            "Loan_Amount_Term INT,"
            "Credit_History INT,"
            "Property_Area VARCHAR(255),"
            "Loan_Status VARCHAR(255)"
            ")"
        )

        cursor.execute(table_schema)
        connection.commit()

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Access denied. Check your credentials.")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist.")
        else:
            print(err)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

create_table()

def get_db():
    connection = mysql.connector.connect(**db_config)
    yield connection
    connection.close()

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...), db: mysql.connector.connection.MySQLConnection = Depends(get_db)):
    try:
        contents = await file.read()
        decoded_contents = contents.decode("utf-8")
        csv_reader = csv.reader(decoded_contents.splitlines(), delimiter=',')
        rows = list(csv_reader)

        cursor = db.cursor()

        # Insert data into MySQL
        for row in rows:
            query = "INSERT INTO loan_data (Loan_ID, Gender, Married, Dependents, Education, Self_Employed, " \
                    "ApplicantIncome, CoapplicantIncome, LoanAmount, Loan_Amount_Term, Credit_History, " \
                    "Property_Area, Loan_Status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(query, tuple(row))

        db.commit()
        cursor.close()

        return JSONResponse(content={"message": "Data successfully inserted into MySQL database"})

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/loan_data/{loan_id}")
async def read_loan_data(loan_id: str, db: mysql.connector.connection.MySQLConnection = Depends(get_db)):
    cursor = db.cursor(dictionary=True)
    query = "SELECT * FROM loan_data WHERE Loan_ID = %s"
    cursor.execute(query, (loan_id,))
    result = cursor.fetchone()
    cursor.close()

    if result:
        return result
    else:
        raise HTTPException(status_code=404, detail="Loan data not found")

@app.put("/loan_data/{loan_id}")
async def update_loan_data(loan_id: str, file: UploadFile = File(...), db: mysql.connector.connection.MySQLConnection = Depends(get_db)):
    cursor = db.cursor()
    
    # Check if the loan data exists
    query = "SELECT * FROM loan_data WHERE Loan_ID = %s"
    cursor.execute(query, (loan_id,))
    result = cursor.fetchone()
    
    if not result:
        cursor.close()
        raise HTTPException(status_code=404, detail="Loan data not found")

    # Update the existing data
    contents = await file.read()
    decoded_contents = contents.decode("utf-8")
    csv_reader = csv.reader(decoded_contents.splitlines(), delimiter=',')
    new_data = list(csv_reader)[0]

    query = "UPDATE loan_data SET Gender=%s, Married=%s, Dependents=%s, Education=%s, Self_Employed=%s, " \
            "ApplicantIncome=%s, CoapplicantIncome=%s, LoanAmount=%s, Loan_Amount_Term=%s, " \
            "Credit_History=%s, Property_Area=%s, Loan_Status=%s WHERE Loan_ID=%s"

    cursor.execute(query, tuple(new_data + [loan_id]))
    db.commit()
    cursor.close()

    return JSONResponse(content={"message": "Data successfully updated"})

@app.delete("/loan_data/{loan_id}")
async def delete_loan_data(loan_id: str, db: mysql.connector.connection.MySQLConnection = Depends(get_db)):
    cursor = db.cursor()

    # Check if the loan data exists
    query = "SELECT * FROM loan_data WHERE Loan_ID = %s"
    cursor.execute(query, (loan_id,))
    result = cursor.fetchone()

    if not result:
        cursor.close()
        raise HTTPException(status_code=404, detail="Loan data not found")

    # Delete the loan data
    query = "DELETE FROM loan_data WHERE Loan_ID = %s"
    cursor.execute(query, (loan_id,))
    db.commit()
    cursor.close()

    return JSONResponse(content={"message": "Data successfully deleted"})

@app.get("/loan_data/married/{married}")
async def read_loan_data_by_married(married: str, db: mysql.connector.connection.MySQLConnection = Depends(get_db)):
    cursor = db.cursor(dictionary=True)
    query = "SELECT * FROM loan_data WHERE Married = %s"
    cursor.execute(query, (married,))
    result = cursor.fetchall()
    cursor.close()

    if result:
        return result
    else:
        raise HTTPException(status_code=404, detail=f"No data found for Married: {married}")
    


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=3000)