from fastapi import APIRouter, Body
from os import environ as env
from typing import List
from pydantic import BaseModel
import db_connection
from fastapi import APIRouter
from typing import Dict
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import pickle
from sklearn.preprocessing import LabelEncoder


router = APIRouter()


class DropdownResponse(BaseModel):
    data: List[str]


connection, cursor, db = db_connection.get_db()

@router.post("/predict")
async def predict(
        # Gender: str = Body(...),
        # Married: str = Body(...),
        # Dependents: int = Body(...),
        # Education: str = Body(...),
        # Self_Employed: str = Body(...),
        # ApplicantIncome: float = Body(...),
        # CoapplicantIncome: float = Body(...),
        # LoanAmount: float = Body(...),
        # Loan_Amount_Term: int = Body(...),
        # Credit_History: float = Body(...),
        # Property_Area: str = Body(...),
):
    try:
        
        le_gender = LabelEncoder()
        le_gender.fit_transform(['Female', 'Male'])

        le_married = LabelEncoder()
        le_married.fit_transform(['No', 'Yes'])

        le_education = LabelEncoder()
        le_education.fit_transform(['Graduate', 'Not Graduate'])

        le_self_employed = LabelEncoder()
        le_self_employed.fit_transform(['No', 'Yes'])

        le_property_area = LabelEncoder()
        le_property_area.fit_transform(['Rural', 'Semiurban', 'Urban'])

        le_loan_status = LabelEncoder()
        le_loan_status.fit_transform(['N', 'Y'])
        
        loaded_model = pickle.load(open('files/pkl/RF_new_data.pkl' , 'rb'))

        test_input = pd.DataFrame({
            'Gender':'Male',
            'Married':'Yes',
            'Dependents':0,
            'Education':'Graduate',
            'Self_Employed':'No',
            'ApplicantIncome':3036,
            'CoapplicantIncome':2504,
            'LoanAmount':15800,
            'Loan_Amount_Term':12,
            'Credit_History':0,
            'Property_Area': 'Semiurban'
        },index=[0])

        test_input['Gender']= le_gender.fit_transform(test_input['Gender'])
        test_input['Married']= le_married.fit_transform(test_input['Married'])
        test_input['Education']= le_education.fit_transform(test_input['Education'])
        test_input['Self_Employed']= le_self_employed.fit_transform(test_input['Self_Employed'])
        test_input['Property_Area']= le_property_area.fit_transform(test_input['Property_Area'])

        result = loaded_model.predict(test_input)
        return le_loan_status.inverse_transform([result])

    except Exception as e:
        return {"error": str(e)}
