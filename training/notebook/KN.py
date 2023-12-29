import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNNClassifier
import joblib
import pickle


df = pd.read_csv('files/csv/dbbl_loan.csv')

# df.head()

df['Address'] = df['Area Name']
df['Schm_Desc'] = df['Schm Desc']
df['Sanct_Lim'] = df['Sanct Lim']

le = LabelEncoder()
df['Address'] = le.fit_transform(df['Address'])
df['Schm_Desc'] = le.fit_transform(df['Schm_Desc'])
df['Status'] = le.fit_transform(df['Status'])
# df.head()

features = ['Address', 'Schm_Desc', 'Rate', 'Sanct_Lim']
target = ['Status']
x = df[features]
y = df[target]
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, shuffle=False)
x_train.head()

mean_rate = df['Rate'].mean()
df['Rate'].fillna(mean_rate, inplace=True)

features = ['Address', 'Schm_Desc', 'Rate', 'Sanct_Lim']
target = ['Status']
x = df[features]
y = df[target]
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, shuffle=False)
x_train.head()

model = KNNClassifier()
model.fit(x_train, y_train)

pickle.dump(model, open('files/pkl/KN.pkl', 'wb'))
