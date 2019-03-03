import pandas as pd
df = pd.read_pickle("text-files/dataframe1.txt")

from sklearn import linear_model
from sklearn.preprocessing import PolynomialFeatures
poly = PolynomialFeatures()
poly.fit_transform(df)
print(df)
reg = linear_model.LinearRegression()
reg.fit(df[['CP','CN','T/F','choice_depth']], df['good_decision'])

print(reg.intercept_,reg.coef_)