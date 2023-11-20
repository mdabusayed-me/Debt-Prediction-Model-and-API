from flask import Flask, jsonify, request
from sklearn.preprocessing import LabelEncoder
import pandas as pd
from flask_cors import CORS 
import joblib
import pickle

app = Flask(__name__)
CORS(app)

df = pd.read_csv('dbbl_loan.csv')

df['Address'] = df['Area Name']

@app.route('/get_addresses', methods=['GET'])
def get_addresses():
    unique_addresses = df['Address'].unique()
    return jsonify({"data": list(unique_addresses)})


@app.route('/get_schm_desc', methods=['GET'])
def get_schm_desc():
    unique_scheme = df['Schm Desc'].unique()
    return jsonify({"data": list(unique_scheme)})

model = pickle.load(open('Randomf.pkl', 'rb'))

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get input data from JSON request
        data = request.get_json()
        # address_label_encoder = LabelEncoder()
        # schm_desc_label_encoder = LabelEncoder()
        # Transform input data using fitted label encoders
        address = data['Address']
        schm_desc = data['Schm_Desc']
        # address = address_label_encoder.transform([data['Address']])
        # schm_desc = schm_desc_label_encoder.transform([data['Schm_Desc']])
        rate = data['Rate']
        sanct_lim = data['Sanct_Lim']
        balance = data['Balance']

        # Make predictions
        input_data = pd.DataFrame({'Address': address, 'Schm_Desc': schm_desc, 'Rate': [rate], 'Sanct_Lim': [sanct_lim], 'Balance': [balance]})
        predictions = model.predict(input_data)

        # Inverse transform the predicted values for 'Status'
        predicted_status = predictions[0]  # Assuming 'Status' is already encoded as integers

        return jsonify({"status": predicted_status})

    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/predict_from_real_field', methods=['POST'])
def predict_real():
    try:

        data = request.get_json()
        # address_label_encoder = LabelEncoder()
        # schm_desc_label_encoder = LabelEncoder()
        # Transform input data using fitted label encoders
        address = data['Address']
        schm_desc = data['Schm_Desc']
        # address = address_label_encoder.transform([data['Address']])
        # schm_desc = schm_desc_label_encoder.transform([data['Schm_Desc']])
        rate = data['Rate']
        sanct_lim = data['Sanct_Lim']
        balance = data['Balance']
    
        label_encoder = LabelEncoder()
        test_input = pd.DataFrame({'Address': [address],'Schm_Desc':[schm_desc],'Rate': [rate], 'Sanct_Lim': [sanct_lim], 'Balance': [balance]})
        test_input['Address']=label_encoder.fit_transform(test_input['Address'])
        test_input['Schm_Desc']=label_encoder.fit_transform(test_input['Schm_Desc'])

       
        # Make predictions
        predictions = model.predict(test_input)
        if predictions >= 5:
            return ("Loan is ok")
        else:
            return ("Loan is doubtful")

    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == '__main__':
    app.run(debug=True)
