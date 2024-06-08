from flask import Flask, render_template, request, session, redirect
import pandas as pd
import numpy as np
from model import Model

df = pd.DataFrame('livability/data/unified.csv')
model = Model(df, 'livability')
def predict(data):
    return Model.predict(data)

app = Flask(__name__)

app.config["SECRET_KEY"] = "may is a pretty princess <3"

@app.route('/', methods=["POST", "GET"])
def index():
    return render_template('index.html')
    
""" user picks their desired city and inputs preferences ->
    system looks up conditions of the city -> 
    model predicts the livabiliy of the city chosen and the preferred conditions separately -> 
    standardize the livability differences and inverse norm to find the % chance of getting the results -> 
    show the user how livable the city is (% multiplied by 100)"""
