from sklearn import linear_model as lm
from sklearn.model_selection import train_test_split
from scipy.stats import norm
from sklearn.metrics import accuracy_score as accuracy
import numpy as np
import pandas as pd

class Model:
    def __init__(self, df, response: str) -> None:
        self.df = df
        self.Y = df[response]
        self.features = df.drop(columns='livability', axis=1)
        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(df, self.Y, test_size=.2, random_state=10)
        self.model = lm.LinearRegression()
    def fit(self) -> None:
        self.model.fit(self.x_train, self.y_train)

    def predict(self,test: iter) -> pd.array:
        return self.model.predict(test)
    
    def score(self, observed, preferred):
        sd = self.sd()
        _zstat = (float(observed['livability']) - float(preferred['livability'])) / (sd / (len(self.df.index) ** 0.5))
        return norm.cdf(_zstat, loc=0, scale=1)[len(norm.cdf(_zstat, loc=0, scale=1)) - 1]
    def sd(self):
        return np.std(self.Y)
    



