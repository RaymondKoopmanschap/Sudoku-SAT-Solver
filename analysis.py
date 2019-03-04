import pandas as pd
import numpy as np
df = pd.read_pickle("text-files/dataframe1.txt")
df['majority_was_picked']=(df['CP']-df['CN'])*df['T/F']>0
print(sum(df['majority_was_picked']))
df['CP'] = df['CP']#/4
df['CN'] = df['CN']#/32
df=df[df.majority_was_picked == 1]
df['CPxCN'] = df['CP']*df['CN']
df['sumCPCN'] = df['CP'] + df['CN']
df['deltaC'] = sum(df['CP'] - df['CN'])


df.to_csv("text-files/processed_dataframe.csv", index=False, encoding='utf8')
from sklearn import linear_model
from sklearn import metrics
print(df)
reg = linear_model.LinearRegression()
X=df[['sumCPCN','CPxCN','maxCPCN','choice_depth']]
y=df['good_decision']
reg.fit(X,y)
print('Normalized Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y, reg.predict(X)))/(max(y)-min(y)))
#print([reg.predict(X)])

print(reg.intercept_,reg.coef_)


print(np.maximum([1,3,5],[4,2,4]))