from sqlalchemy import create_engine
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib
import pickle


df = pd.read_csv('files/csv/dbbl_loan.csv')

# df.head()

df['Address']= df['Area Name']
df['Schm_Desc']= df['Schm Desc']
df['Sanct_Lim']= df['Sanct Lim']

le = LabelEncoder()
df['Address'] = le.fit_transform(df['Address'])
df['Schm_Desc'] = le.fit_transform(df['Schm_Desc'])
df['Status'] = le.fit_transform(df['Status'])
# df.head()


features=['Address','Schm_Desc','Rate','Sanct_Lim']
target=['Status']
x=df[features]
y=df[target]
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, shuffle=False)
x_train.head()

mean_rate = df['Rate'].mean()
df['Rate'].fillna(mean_rate, inplace=True)

features=['Address','Schm_Desc','Rate','Sanct_Lim']
target=['Status']
x=df[features]
y=df[target]
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, shuffle=False)
x_train.head()


model  = RandomForestClassifier()
model.fit(x_train, y_train)

# label_encoder = LabelEncoder()
# test_input = pd.DataFrame({'Address': ['Amborkhana'],'Schm_Desc':['HOME CREDIT'],'Rate': [9], 'Sanct_Lim': [11000000]})
# test_input['Address']=label_encoder.fit_transform(test_input['Address'])
# test_input['Schm_Desc']=label_encoder.fit_transform(test_input['Schm_Desc'])

# # Make predictions
# predictions = model.predict(test_input)
# if predictions >= 5:
#   print("Loan is ok")
# else:
#   print("Loan is doubtful")
# prediction_probabilities = model.predict_proba(test_input)



# confidence = prediction_probabilities[0][predictions[0]] * 100

# print(f"Confidence: {confidence:.2f}%")

# # Make a decision based on confidence level
# threshold = 0.7  # Adjust this threshold based on your preference
# if confidence >= threshold:
#     print("Loan is ok")
# else:
#     print("Loan is doubtful")

pickle.dump(model , open('files/pkl/model_RF_1.pkl' , 'wb'))