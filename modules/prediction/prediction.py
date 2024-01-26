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
            classification_models['KNNClassifier']: 'files/pkl/KNNClassifier.pkl',
            # classification_models['LogisticRegression']: 'files/pkl/LogisticRegression.pkl',
            # classification_models['NaiveBayes']: 'files/pkl/NaiveBayes.pkl',
            classification_models['RandomForestClassifier']: 'files/pkl/RandomForestClassifier.pkl',
            # classification_models['SupportVectorClassifier']: 'files/pkl/SupportVectorClassifier.pkl',
            # classification_models['RandomForestRegressor']: 'files/pkl/RFRegression.pkl'
        }

        predictions_array = []
        for model in data.selected_model:
            if model in model_files:
                loaded_model = pickle.load(open(model_files[model], 'rb'))
                input_data_df = pd.DataFrame([data.model_dump()])

                input_data_df = pd.get_dummies(input_data_df, columns=['gender', 'married', 'dependents', 'education', 'self_employed', 'property_area'])

                input_data_df = input_data_df.reindex(columns=loaded_model.feature_names_in_, fill_value=0)

                prediction = loaded_model.predict(input_data_df)

                # Find the accuracy info for the current model from the JSON data
                accuracy_info = next((entry for entry in model_accuracy_data if entry["algorithm_name"] == model), None)

                if accuracy_info:
                    predictions_array.append({
                        "result": prediction[0],
                        "model": model,
                        "algorithm_type": accuracy_info["algorithm_type"],
                        "accuracy_score": accuracy_info["accuracy_score"],
                        "precision_score": accuracy_info["precision_score"],
                        "recall_score": accuracy_info["recall_score"],
                        "f1_score": accuracy_info["f1_score"],
                        "support": accuracy_info["support"]
                    })
            
            else:
                predictions_array.append("Model not found")

        return {"data": predictions_array}

    except Exception as e:
        return {"error": str(e)}
