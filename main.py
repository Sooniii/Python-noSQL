import os

from flask import Flask
from flask import request
from flask import make_response

app = Flask(__name__)

@app.route("/user", methods=["GET"])
def show_users():
    reponse = ""
    folder = os.listdir("./user")
    #print(folder)

    for item in folder:
        print(item)
        texte = open("./user/"+item, 'r')
        user = texte.readline()
        reponse = reponse + user
        texte.close()

    return make_response(reponse,200)



@app.route("/", methods=["GET","POST"])
def acceuil():

    if request.method == "GET":
        pass
    elif request.method == "POST":
        pass

    print(f"arguments : {request.args}")
    print(f"body: {request.get_json()}")

    body = " Je fonctionne "
    return make_response(body,200)

if(__name__) == '__main__':
    app.run(
        host = "0.0.0.0",
        port=8081,
        debug=True,
    )
