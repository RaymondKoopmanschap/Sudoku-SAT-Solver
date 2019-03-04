import pandas as pd
import numpy as np
df = pd.read_pickle("text-files/dataframe1.txt")

df['CP'] = df['CP']/df['max_C']
df['CN'] = df['CN']/df['max_C']
df['prodC'] = df['CP']*df['CN']
df['sumC'] = df['CP'] + df['CN']
df['deltaC'] = abs(df['CP'] - df['CN'])

df['JP'] = df['CP']/df['max_C']
df['JN'] = df['CN']/df['max_C']
df['prodJ'] = df['CP']*df['CN']
df['sumJ'] = df['CP'] + df['CN']
df['deltaJ'] = abs(df['CP'] - df['CN'])

df['fP'] = df['CP']/df['max_C']
df['fN'] = df['CN']/df['max_C']
df['prodf'] = df['CP']*df['CN']
df['sumf'] = df['CP'] + df['CN']
df['deltaf'] = abs(df['CP'] - df['CN'])


df.to_csv("text-files/processed_dataframe.csv", index=False, encoding='utf8')
from sklearn import linear_model
from sklearn import metrics
print(df)
reg = linear_model.LinearRegression()
X=df[['sumC','prodC','deltaC','sumJ','prodJ','deltaJ','sumf','prodf','deltaf','choice_depth','num_unsat_clauses']]
y=df['good_decision']
reg.fit(X,y)
print('Normalized Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y, reg.predict(X)))/(max(y)-min(y)))
#print([reg.predict(X)])

print(reg.intercept_,reg.coef_)


print(np.maximum([1,3,5],[4,2,4]))