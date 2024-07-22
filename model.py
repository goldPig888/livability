import joblib
from scipy.stats import norm
from sklearn import linear_model as lm
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import pandas as pd

class Model:
    def __init__(self, df, response: str) -> None:
        if df is not None:
            self.df = df
            self.Y = df[response]
            self.features = df.drop(columns=response, axis=1)
            self.feature_names = self.features.columns.tolist()
            self.scaler_x = MinMaxScaler()
            self.scaler_y = MinMaxScaler(feature_range=(0, 100))
            self.features = pd.DataFrame(self.scaler_x.fit_transform(self.features), columns=self.feature_names)
            self.Y = self.scaler_y.fit_transform(self.Y.values.reshape(-1, 1)).flatten()
            self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(self.features, self.Y, test_size=0.2, random_state=10)
        else:
            self.df = self.Y = self.features = self.feature_names = self.x_train = self.x_test = self.y_train = self.y_test = None
            self.scaler_x = self.scaler_y = None
        self.model = lm.LinearRegression()

    def fit(self) -> None:
        self.model.fit(self.x_train, self.y_train)

    def predict(self, test: pd.DataFrame) -> np.ndarray:
        test_scaled = self.scaler_x.transform(test)
        predictions = self.model.predict(test_scaled)
        return self.scaler_y.inverse_transform(predictions.reshape(-1, 1)).flatten()

    def save_model(self, path: str) -> None:
        joblib.dump((self.model, self.df, self.feature_names, self.scaler_x, self.scaler_y), path)

    def load_model(self, path: str) -> None:
        self.model, self.df, self.feature_names, self.scaler_x, self.scaler_y = joblib.load(path)
        self.Y = self.df['livability']
        self.features = self.df.drop(columns='livability', axis=1)

    def score(self, observed, preferred):
        sd = self.sd()
        _zstat = (float(observed['livability']) - float(preferred['livability'])) / (sd / (len(self.df.index) ** 0.5))
        return norm.cdf(_zstat, loc=0, scale=1)[-1]

    def sd(self):
        return np.std(self.Y)
