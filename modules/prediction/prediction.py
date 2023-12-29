import pickle
from os import environ as env
from typing import Dict, List

import pandas as pd
from fastapi import APIRouter, Body
from pydantic import BaseModel
from sklearn.preprocessing import LabelEncoder

import db_connection
from config.constant import classification_models

router = APIRouter()


class DropdownResponse(BaseModel):
    data: List[str]


connection, cursor, db = db_connection.get_db()

@router.post("/predict")
async def predict(
        gender: str = Body(...),
        married: str = Body(...),
        dependents: int = Body(...),
        education: str = Body(...),
        self_employed: str = Body(...),
        applicantIncome: float = Body(...),
        coapplicant_income: float = Body(...),
        loan_amount: float = Body(...),
        loan_amount_term: int = Body(...),
        credit_history: float = Body(...),
        property_area: str = Body(...),
        selected_model: str = Body(...),
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


        model_files = {
            classification_models['KNNClassifier']: 'files/pkl/KNNClassifier.pkl',
            classification_models['LogisticRegression']: 'files/pkl/LogisticRegression.pkl',
            classification_models['NaiveBayes']: 'files/pkl/NaiveBayes.pkl',
            classification_models['RandomForestClassifier']: 'files/pkl/RandomForestClassifier.pkl',
            classification_models['SupportVectorClassifier']: 'files/pkl/SupportVectorClassifier.pkl'
        }

        if selected_model in model_files:
            loaded_model = pickle.load(open(model_files[selected_model], 'rb'))
        else:
            return {"error": "Model not found"}
        
        test_input = pd.DataFrame({
            'gender': gender,
            'married': married,
            'dependents': dependents,
            'education': education,
            'self_employed': self_employed,
            'applicantIncome': applicantIncome,
            'coapplicant_income': coapplicant_income,
            'loan_amount': loan_amount,
            'loan_amount_term': loan_amount_term,
            'credit_history': credit_history,
            'property_area': property_area
        }, index=[0])

        test_input['gender']= le_gender.fit_transform(test_input['gender'])
        test_input['married']= le_married.fit_transform(test_input['married'])
        test_input['education']= le_education.fit_transform(test_input['education'])
        test_input['self_employed']= le_self_employed.fit_transform(test_input['self_employed'])
        test_input['property_area']= le_property_area.fit_transform(test_input['property_area'])

        result = loaded_model.predict(test_input)

        # print(le_loan_status.inverse_transform(result.ravel()))
        return {"data": le_loan_status.inverse_transform(result.ravel())[0]}

    except Exception as e:
        return {"error": str(e)}
