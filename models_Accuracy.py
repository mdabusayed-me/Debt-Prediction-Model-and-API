import json
import pickle
from typing import List

import pandas as pd
from fastapi import APIRouter, Body
from pydantic import BaseModel
from sklearn.preprocessing import LabelEncoder
from sklearn import metrics

router = APIRouter()


class DropdownResponse(BaseModel):
    data: List[str]


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
        # Load the model from the pickle file
        model_path = f'files/pkl/{selected_model}.pkl'
        loaded_model = pickle.load(open(model_path, 'rb'))

        # Preprocess the input features
        le_gender = LabelEncoder()
        le_married = LabelEncoder()
        # ... (add other label encoders)

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

        test_input['gender'] = le_gender.fit_transform(test_input['gender'])
        test_input['married'] = le_married.fit_transform(test_input['married'])
        # ... (transform other categorical features)

        # Make predictions
        result = loaded_model.predict(test_input)

        # Calculate various classification metrics
        accuracy_score = metrics.accuracy_score(y_test, result)
        precision_score = metrics.precision_score(y_test, result)
        recall_score = metrics.recall_score(y_test, result)
        f1_score = metrics.f1_score(y_test, result)
        confusion_matrix = metrics.confusion_matrix(y_test, result).tolist()

        # Construct the result dictionary
        result_dict = {
            "result": result,
            "model": selected_model,
            "algorithm_type": "Classification",
            "accuracy_score": accuracy_score,
            "precision_score": precision_score,
            "recall_score": recall_score,
            "f1_score": f1_score,
            "confusion_matrix": confusion_matrix
        }

        return {"data": result_dict}

    except Exception as e:
        return {"error": str(e)}
