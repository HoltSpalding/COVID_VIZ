from flask import Flask, render_template, request, jsonify, send_from_directory
import random,os, json,sys
import pandas as pd 
from app.getCoronaData import getConfirmedGivenDate,assignColors

#Save corona data in DataFrame
df = pd.read_csv("app/static/us_corona_counties.csv")
df = df.drop("UID",axis=1).drop("iso2",axis=1).drop("iso3",axis=1).drop("code3",axis=1).drop("Country_Region",axis=1)
#Confirmed cases stats
max_confirmed = df["Confirmed"].max()
mean_confirmed = df["Confirmed"].mean()
std_confirmed = df["Confirmed"].std()

app = Flask(__name__,template_folder='templates') 

@app.route("/") 
def index(): 
    return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),'favicon.ico')

@app.route('/usjson')
def usjson():
    return send_from_directory(os.path.join(app.root_path, 'static'),'us.json')


@app.route("/get_map_data", methods=["POST"])
def get_map_data():
    if request.method == "POST":
        assert(request.is_json)
        date = request.get_json()["date"]
        confirmed_given_date = getConfirmedGivenDate(df, date)
        return assignColors(confirmed_given_date,0,max_confirmed,mean_confirmed,std_confirmed)