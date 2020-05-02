from flask import Flask, render_template, request, jsonify 
import random 

app = Flask(__name__,template_folder='templates') 




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
        return "s"
        # print(request.data.decode('UTF-8'))
        # print(".................")
        # print(request.data)
        # print(".................")
        # return request.data

