from flask import Flask, request, jsonify, make_response
import pickle
import pandas as pd
from flask_cors import CORS, cross_origin


#create Flask App
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'



# Load the save mode
# model_rf = pickle.load(open('Randomf.pkl', 'rb'))
model_rf = pickle.load(open('Randomf_jubair.pkl', 'rb'))
model_nb = pickle.load(open('Naivb.pkl', 'rb'))
model_knei = pickle.load(open('KNei.pkl', 'rb'))
model_dt = pickle.load(open('DecisionTree.pkl', 'rb'))



#create API Routing call for RandomForest Classifier

@app.route('/predict_rf', methods= ['POST'])
@cross_origin()
def predict_rf():
    # GET JSON Request
    test_input = request.json
    df = pd.DataFrame(test_input)
    # # GET Prediction
    prediction = model_rf.predict(df)
    #retrun JSON Version of Prediction
    return jsonify({'prediction': float(prediction)})



#create API Routing call for Naib Bayes
@app.route('/predict_nb', methods= ['POST'])
@cross_origin()
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


#create API Routing call Decision Tree
@app.route('/predict_dt', methods= ['POST'])
def predict_dt():
    # GET JSON Request
    test_input = request.json
    df = pd.DataFrame(test_input)
    # GET Prediction
    prediction = model_dt.predict(df)
    #retrun JSON Version of Prediction
    return jsonify({'prediction': float(prediction)})



<<<<<<< HEAD
def _build_cors_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response

def _corsify_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


if __name__ == "__main__":
    app.run(debug=True, host= '0.0.0.0', port=12345)
=======

app.run(debug=True, host= '0.0.0.0', port=12345)
>>>>>>> 86e07fa (api created for address and scheme)
