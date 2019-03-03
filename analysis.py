import pandas as pd
df = pd.read_pickle("text-files/dataframe1.txt")
df['majority_was_picked']=(df['CP']-df['CN'])*df['T/F']>0
print(sum(df['majority_was_picked']))
df['CP'] = df['CP']/4
df['CN'] = df['CN']/32
df=df[df.majority_was_picked == 1]
df['CPxCN'] = df['CP']*df['CN']
df['Delta_C'] = abs(df['CP'] - df['CN'])
df.to_csv("text-files/processed_dataframe.csv", index=False, encoding='utf8')
from sklearn import linear_model
from sklearn.preprocessing import PolynomialFeatures
#poly = PolynomialFeatures()
#poly.fit_transform(df)
print(df)
reg = linear_model.LinearRegression()
reg.fit(df[['CP','CN','CPxCN','Delta_C','choice_depth']], df['good_decision'])
print(reg.intercept_,reg.coef_)