from flask import Flask, render_template, request, jsonify, send_from_directory
import random,os 

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

