import pandas as pd
from sklearn.preprocessing import LabelEncoder
import pickle

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

# model = joblib.load('loan_status_predict')
# for Y
# LP001002,Male,No,0,Graduate,No,5849,0,12000,12,1,Urban,Y
test_input = pd.DataFrame({
    'Gender':'Male',
    'Married':'No',
    'Dependents':0,
    'Education':'Graduate',
    'Self_Employed':'No',
    'ApplicantIncome':5849,
    'CoapplicantIncome':0,
    'LoanAmount':12000,
    'Loan_Amount_Term':12,
    'Credit_History':1,
    'Property_Area': 'Urban'
},index=[0])

# for N
# LP001014,Male,Yes,0,Graduate,No,3036,2504,15800,12,0,Semiurban,N
# test_input = pd.DataFrame({
#     'Gender':'Male',
#     'Married':'Yes',
#     'Dependents':0,
#     'Education':'Graduate',
#     'Self_Employed':'No',
#     'ApplicantIncome':3036,
#     'CoapplicantIncome':2504,
#     'LoanAmount':15800,
#     'Loan_Amount_Term':12,
#     'Credit_History':0,
#     'Property_Area': 'Semiurban'
# },index=[0])

test_input['Gender']= le_gender.fit_transform(test_input['Gender'])
test_input['Married']= le_married.fit_transform(test_input['Married'])
test_input['Education']= le_education.fit_transform(test_input['Education'])
test_input['Self_Employed']= le_self_employed.fit_transform(test_input['Self_Employed'])
test_input['Property_Area']= le_property_area.fit_transform(test_input['Property_Area'])

result = loaded_model.predict(test_input)

print(le_loan_status.inverse_transform(result.ravel()))
