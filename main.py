import os

from flask import Flask
from flask import request
from flask import make_response

app = Flask(__name__)


# @app.route("/", methods=["GET","POST"])
def acceuil():
    if request.method == "GET":
        pass
    elif request.method == "POST":
        pass

    print(f"arguments : {request.args['id']}")
    print(f"body: {request.get_json()}")

    body = " Je fonctionne "
    return make_response(body, 200)


"""
affiche les utilisateur
params:none
return: une reponse avec le nom utilisateur


"""


@app.route("/user", methods=["GET"])
def show_users():
    reponse = ""
    folder = os.listdir("./user")
    # print(folder)

    for item in folder:
        texte = open("./user/" + item, 'r')
        user = texte.readline()
        reponse = reponse + user
        texte.close()

    return make_response(reponse, 200)


"""
ajoute un utilisateur
params: newUser(un json avec le nom et le prenom d'un nouvel utilisateur)
"""


@app.route("/adduser", methods=["POST"])
def add_user():
    name = request.get_json()
    index = f"{request.args['id']}"
    print("./user/"+index+".txt")
    if os.path.exists("./user/"+index+".txt") == False:
        file = open("./user/"+index+".txt",'x')
        file.write(name['nom']+"\n"+name['prenom'])
        file.close()
    else:
        name = "l'utilisateur existe deja"
    return make_response(name, 200)


if (__name__) == '__main__':
    app.run(
        host="0.0.0.0",
        port=8081,
        debug=True,
    )

    """
    on cherche a modifier un utilisateur
    params:
    """

@app.route("/modifyuser", methods=["PATCH"])
def patch_user():


    return

if (__name__) == '__main__':
    app.run(
        host="0.0.0.0",
        port=8081,
        debug=True,
    )
