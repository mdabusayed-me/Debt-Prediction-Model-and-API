from sqlalchemy import create_engine
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
import joblib 
import pickle


# Connect to the database
engine = create_engine("mysql+mysqlconnector://root:@localhost/debt_db")
# Test the connection
connection = engine.connect()
Query = "SELECT * FROM loans"
df = pd.read_sql_query(Query, connection)
df

le = LabelEncoder()
df['Address'] = le.fit_transform(df['Address'])
df['Schm_Desc'] = le.fit_transform(df['Schm_Desc'])
df['Status'] = le.fit_transform(df['Status'])



features=['Address','Schm_Desc','Rate','Sanct_Lim']
target=['Balance']
x=df[features]
y=df[target]
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, shuffle=False)
x_train.head()

model  = KNeighborsClassifier()
model.fit(x_train, y_train)


label_encoder = LabelEncoder()
test_input = pd.DataFrame({'Address': ['Amborkhana'],'Schm_Desc':['PERSONAL LOAN'],'Rate': [4], 'Sanct_Lim': [100000]})
test_input['Address']=label_encoder.fit_transform(test_input['Address'])
test_input['Schm_Desc']=label_encoder.fit_transform(test_input['Schm_Desc'])

model.predict(test_input)


# joblib.dump(model, 'RandormForest_Classifier.joblib')

# model = joblib.load('RandormForest_Classifier.joblib')

# model.predict(test_input)
pickle.dump(model , open('Knei.pkl' , 'wb'))
loaded_model = pickle.load(open('Knei.pkl' , 'rb'))
loaded_model.predict(test_input)

