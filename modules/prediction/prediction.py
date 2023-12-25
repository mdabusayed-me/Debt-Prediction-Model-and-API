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


router = APIRouter()


class DropdownResponse(BaseModel):
    data: List[str]


connection, cursor, db = db_connection.get_db()

@router.post("/predict")
async def predict(
        Gender: str = Body(...),
        Married: str = Body(...),
        Dependents: int = Body(...),
        Education: str = Body(...),
        Self_Employed: str = Body(...),
        ApplicantIncome: float = Body(...),
        CoapplicantIncome: float = Body(...),
        LoanAmount: float = Body(...),
        Loan_Amount_Term: int = Body(...),
        Credit_History: float = Body(...),
        Property_Area: str = Body(...),
):
    try:
        new_data = pd.DataFrame({
            "Gender": [Gender],
            "Married": [Married],
            "Dependents": [Dependents],
            "Education": [Education],
            "Self_Employed": [Self_Employed],
            "ApplicantIncome": [ApplicantIncome],
            "CoapplicantIncome": [CoapplicantIncome],
            "LoanAmount": [LoanAmount],
            "Loan_Amount_Term": [Loan_Amount_Term],
            "Credit_History": [Credit_History],
            "Property_Area": [Property_Area],
            "Loan_Status": ['N'],
        })

        label_encoder = LabelEncoder()

        new_data['Self_Employed'].fillna('Not Given', inplace=True)
        new_data['Gender'].fillna('Not Given', inplace=True)
        new_data['Dependents'].fillna('Not Given', inplace=True)

        new_data['Gender']= label_encoder.fit_transform(new_data['Gender'])
        new_data['Married']= label_encoder.fit_transform(new_data['Married'])
        new_data['Dependents']= label_encoder.fit_transform(new_data['Dependents'])
        new_data['Education']= label_encoder.fit_transform(new_data['Education'])
        new_data['Self_Employed']= label_encoder.fit_transform(new_data['Self_Employed'])
        new_data['Property_Area']= label_encoder.fit_transform(new_data['Property_Area'])


        new_data['Loan_Status']='Not Given'
        # new_data['Loan_Status']= 'Not Given'
        new_data['Loan_Status'] = label_encoder.fit_transform(new_data['Loan_Status'])

        loaded_model = pickle.load(open('pkl_files/Randomf_dataset_2_train.pkl' , 'rb'))

        loaded_model.predict(new_data.drop(['Loan_Status'], axis=1))


    except Exception as e:
        return {"error": str(e)}
