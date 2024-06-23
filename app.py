from flask import Flask, render_template, request, session, redirect
import pandas as pd
import numpy as np
from model import Model
import psycopg2 as pg

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


@app.route('/preferences', methods=['POST', 'GET'])
def setPreferences():
    colnames = ["city","districts","state","Environmental Stance","aqi","idx","Latitude","Longitude","carbon_intensity",'temp_f','is_day','wind_mph','wind_degree','pressure_in','precip_in','humidity','cloud','feelslike_f','windchill_f','heatindex_f','dewpoint_f','vis_miles','uv','gust_mph', 'aqi', 'idx']
    if request.method == "POST":
        if not session.get('loggedin'):
            return redirect('/login')
        for col in colnames:
            session[f"pref_{col}"] = request.form.get(col)
        
    if request.method == "GET":
        return render_template('preferences.html', prefs = {f'pref_{col}': session.get(f'pref_{col}') for col in colnames})

@app.route('/livability', methods=['POST', 'GET'])
def getScore():
    colnames = ["city","districts","state","Environmental Stance","aqi","idx","Latitude","Longitude","carbon_intensity",'temp_f','is_day','wind_mph','wind_degree','pressure_in','precip_in','humidity','cloud','feelslike_f','windchill_f','heatindex_f','dewpoint_f','vis_miles','uv','gust_mph', 'aqi', 'idx']
    if request.method == 'POST':
        if not session.get('loggedin'):
            return redirect('/login')
        df_pred = pd.DataFrame([session.get(f'pref_{col}') for col in colnames])
        _predScore = model.predict(df_pred)
        df_loc = pd.DataFrame([col for col in colnames])
        _locScore = model.predict(df_loc)
        
        score: float = model.score(_locScore, _predScore)
        
        return render_template('summary.html', score = score)
    
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST': 
        server = pg.connect()
        cursor = server.cursor()
        email = request.form.get('email')
        pw = request.form.get('password')
        cursor.execute('SELECT * FROM accounts WHERE email = %s', email)
        account = cursor.fetchone()
        if not account:
            return redirect('/signup')
        if not account[2]:
            return render_template('login.html', msg = 'You have not verified this email yet. Please sign on to your email and follow the instructions provided in the email that we sent to you. If you continue to have issues, please email us using this email at envindex@gmail.com')
      q      