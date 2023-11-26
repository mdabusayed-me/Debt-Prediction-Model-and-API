from sqlalchemy import create_engine
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib 
import pickle


# Connect to the database
engine = create_engine("mysql+mysqlconnector://root:@localhost/debt_db")
# Test the connection
connection = engine.connect()
Query = "SELECT * FROM loans"
df = pd.read_sql_query(Query, connection)

print(df.head())
print(df.shape)
print(type(df))
print(df.describe())

df.isnull().sum
print(df['Address'].value_counts())
print(df['Schm_Desc'].value_counts())
print(df['Status'].value_counts())


le = LabelEncoder()
df['Address'] = le.fit_transform(df['Address'])
print(df['Address'])
df['Schm_Desc'] = le.fit_transform(df['Schm_Desc'])
print(df['Schm_Desc'])
df['Status'] = le.fit_transform(df['Status'])
print(df['Status'])



features=['Address','Schm_Desc','Rate','Sanct_Lim']
target=['Status']
x=df[features]
y=df[target]
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, shuffle=False)
x_train.head()

model  = RandomForestClassifier()
model.fit(x_train, y_train)


label_encoder = LabelEncoder()
test_input = pd.DataFrame({'Address': ['Amborkhana'],'Schm_Desc':['PERSONAL LOAN'],'Rate': [4], 'Sanct_Lim': [100000]})
test_input['Address']=label_encoder.fit_transform(test_input['Address'])
test_input['Schm_Desc']=label_encoder.fit_transform(test_input['Schm_Desc'])


model.predict(test_input)

# joblib.dump(model, 'DecisionTree.joblib')

# model = joblib.load('DecisionTree.joblib')
# model.predict(test_input)
pickle.dump(model , open('rfp.pkl' , 'wb'))
loaded_model = pickle.load(open('rfp.pkl' , 'rb'))
loaded_model.predict(test_input)
