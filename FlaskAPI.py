from flask import Flask, request, jsonify
import pickle
import pandas as pd
from flask_cors import CORS


#create Flask App
app = Flask(__name__)
CORS(app)


# Load the save mode
model_rf = pickle.load(open('Randomf.pkl', 'rb'))
model_nb = pickle.load(open('Naivb.pkl', 'rb'))
model_knei = pickle.load(open('KNei.pkl', 'rb'))


#create API Routing call for RandomForest Classifier
@app.route('/predict', methods= ['POST'])
def predict():
    # GET JSON Request
    test_input = request.json

    df = pd.DataFrame(test_input)
    # GET Prediction
    prediction = model_rf.predict(df)
    #retrun JSON Version of Prediction
    return jsonify({'prediction': float(prediction)})



#create API Routing call for Naib Bayes
@app.route('/predict_nb', methods= ['POST'])
def predict_nb():
    # GET JSON Request
    test_input = request.json

    df = pd.DataFrame(test_input)
    # GET Prediction
    prediction = model_nb.predict(df)
    #retrun JSON Version of Prediction
    return jsonify({'prediction': float(prediction)})



#create API Routing call Knei
@app.route('/predict_knei', methods= ['POST'])
def predict_knei():
    # GET JSON Request
    test_input = request.json

    df = pd.DataFrame(test_input)
    # GET Prediction
    prediction = model_knei.predict(df)
    #retrun JSON Version of Prediction

    return jsonify({'prediction': float(prediction)})



if __name__ == "__main__":
    app.run(debug=True, host= '0.0.0.0', port=12345)