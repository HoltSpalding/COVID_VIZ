from flask import Flask, render_template, request, jsonify 
import random 

app = Flask(__name__,template_folder='templates') 




@app.route("/") 
def index(): 
    return render_template('index.html')


@app.route("/getdata")
def getdata():
    color = random.choice(["red","blue","green"])
    return jsonify(color)

