import json
import pickle
from os import environ as env
from typing import Dict, List
from sklearn import metrics
import pandas as pd
from fastapi import APIRouter, Body
from pydantic import BaseModel
from sklearn.preprocessing import LabelEncoder

import db_connection
from config.constant import classification_models

with open('files/others/accuracy.json', 'r') as file:
    model_accuracy_data = json.load(file)


router = APIRouter()


class DropdownResponse(BaseModel):
    data: List[str]


# Define the input data model using Pydantic
class InputData(BaseModel):
    married: str= Body(...)
    gender: str= Body(...)
    dependents: str= Body(...)
    education: str= Body(...)
    self_employed: str= Body(...)
    applicantIncome: float= Body(...)
    coapplicant_income: float= Body(...)
    loan_amount: float= Body(...)
    loan_amount_term: float= Body(...)
    credit_history: float= Body(...)
    property_area: str= Body(...)
    selected_model: List[str] = Body(...)


connection, cursor, db = db_connection.get_db()


@router.post("/predict")
async def predict(
        data: InputData
):
    try:

        model_files = {
            # classification_models['DecisionTreeClassifier']: 'files/pkl/DecisionTreeClassifier.pkl',
            # classification_models['KNNClassifier']: 'files/pkl/KNNClassifier.pkl',
            # classification_models['LogisticRegression']: 'files/pkl/LogisticRegression.pkl',
            # classification_models['NaiveBayes']: 'files/pkl/NaiveBayes.pkl',
            classification_models['RandomForestClassifier']: 'files/pkl/RandomForestClassifier.pkl',
            classification_models['SupportVectorClassifier']: 'files/pkl/SupportVectorClassifier.pkl',
            classification_models['RandomForestRegressor']: 'files/pkl/RFRegression.pkl'
        }

        predictions_array = []
        for model in data.selected_model:
            if model in model_files:
                loaded_model = pickle.load(open(model_files[model], 'rb'))
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

                test_input['gender'] = le_gender.fit_transform(
                    test_input['gender'])
                test_input['married'] = le_married.fit_transform(
                    test_input['married'])
                test_input['education'] = le_education.fit_transform(
                    test_input['education'])
                test_input['self_employed'] = le_self_employed.fit_transform(
                    test_input['self_employed'])
                test_input['property_area'] = le_property_area.fit_transform(
                    test_input['property_area'])

                result = loaded_model.predict(test_input).astype(int)
                # # Find the accuracy info for the current model from the JSON data
                accuracy_info = next((entry for entry in model_accuracy_data if entry["algorithm_name"] == model), None)

                predictions_array.append({
                    "result": le_loan_status.inverse_transform(result.ravel())[0],
                    "model": model,
                    "algorithm_type": "Classification",
                    "accuracy_score": "0.9193548387096774",
                    "precision_score": "0.93",
                    "recall_score": "0.92",
                    "f1_score": "0.91",
                    "support": "62"
                })
            else:
                predictions_array.append("Model not found")

        return {"data": predictions_array}

    except Exception as e:
        return {"error": str(e)}
