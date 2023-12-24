import psycopg2
from os import environ as env
from typing import List
from pydantic import BaseModel
import db_connection
from fastapi import APIRouter, Path

router = APIRouter()

class DropdownResponse(BaseModel):
    data: List[str]

connection, cursor, db = db_connection.get_db()

def get_distinct_values(column_name: str):
    query = f"SELECT DISTINCT {column_name} FROM loan_train_data WHERE {column_name} IS NOT NULL"
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()

    # Extract the distinct values
    values = [row[0] for row in data]

    return {"data": values}

@router.get("/{columnName}", response_model=DropdownResponse)
async def get_loan_train_data_dropdown(
    columnName: str = Path(..., description="Allowed parameters: gender, self_employed, education, married")
):
    allowed_columnNames = ["gender", "self_employed", "education", "married"]
    if columnName not in allowed_columnNames:
        return {"data": []}
    
    return get_distinct_values(columnName)