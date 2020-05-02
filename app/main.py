from flask import Flask, render_template, request, jsonify, send_from_directory
import random,os, json,sys
import pandas as pd 
from app.getCoronaData import getConfirmedGivenDate,assignColors

df = pd.read_csv("app/static/us_corona_counties.csv")

df = df.drop("UID",axis=1).drop("iso2",axis=1).drop("iso3",axis=1).drop("code3",axis=1).drop("Country_Region",axis=1)

max_confirmed = df["Confirmed"].max()

app = Flask(__name__,template_folder='templates') 



@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),'favicon.ico')

@app.route('/usjson')
def usjson():
    return send_from_directory(os.path.join(app.root_path, 'static'),'us.json')

@app.route("/") 
def index(): 
    return render_template('index.html')



@app.route("/getdata", methods=["GET","POST"])
def getdata():
    if request.method == 'GET':
        color = random.choice(["red","blue","green"])
        return jsonify(color)
    if request.method == "POST":
        print (request.is_json)
        content = request.get_json()
        print (content)
        print(content["data"])
        return content["data"]
        # print(request.data.decode('UTF-8'))
        # print(".................")
        # print(request.data)
        # print(".................")
        # return request.data




@app.route("/getmapdata", methods=["GET","POST"])
def getmapdata():
    if request.method == 'GET':
        return df.to_json()
    if request.method == "POST":
        assert(request.is_json)
        date = request.get_json()["date"]
        # print(date)
        confirmed_given_date = getConfirmedGivenDate(df, date)
        # print(confirmed_given_date)
        # print(max_confirmed)
        return assignColors(confirmed_given_date,0,max_confirmed)
        # print(confirmed_given_date)
        # return confirmed_given_date