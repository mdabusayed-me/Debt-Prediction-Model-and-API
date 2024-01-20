from fastapi import HTTPException, Depends, FastAPI, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from pydantic import BaseModel, Field, ValidationError
from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import pandas as pd

app = FastAPI()

# Load the trained model
with open('random_forest_model.pkl', 'rb') as file:
    model = pickle.load(file)

# Define the input data model using Pydantic
class InputData(BaseModel):
    applicantIncome: float
    coapplicant_income: float
    loan_amount: float
    loan_amount_term: float
    credit_history: float
    gender: str
    married: str
    dependents: str
    education: str
    self_employed: str
    property_area: str

# Define the prediction route
@app.post("/predict")
async def predict(data: InputData):
    try:
        # Convert input data to DataFrame
        input_data_df = pd.DataFrame([data.dict()])

        # Convert categorical variables to dummy/indicator variables
        input_data_df = pd.get_dummies(input_data_df, columns=['gender', 'married', 'dependents', 'education', 'self_employed', 'property_area'])

        # Ensure the order of columns matches the order during training
        input_data_df = input_data_df.reindex(columns=model.feature_names_in_, fill_value=0)

        # Make predictions using the loaded model
        prediction = model.predict(input_data_df)

        return {"prediction": (prediction[0])}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    


    
if __name__ == "__main__":
    app.run(debug=True)