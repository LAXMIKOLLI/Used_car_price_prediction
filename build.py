import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import pickle
from sklearn.model_selection import train_test_split

df = pd.read_csv('final_data.csv')

X = df.drop('Price',axis=1)
y = df['Price']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=1)

rf_reg = RandomForestRegressor(random_state=1)
rf_reg.fit( X_train, y_train)

f=open('model_rf_reg.pkl','wb')
pickle.dump(rf_reg,f)
f.close()
