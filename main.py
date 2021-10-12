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
        name = texte.readline()
        lastname = texte.readline()
        reponse = "<p>" + reponse + name + "\n" + lastname + "</p>" + "\n"
        texte.close()

    return make_response(reponse, 200)

    """
    modifer un utilisateur
    params: User (un json avec le nom et le prenom d'un utilisateur)
    return : le json modifer
    """


@app.route("/modifyUser", methods=["PATCH"])
def patch_user():
    name = request.get_json()
    index = f"{request.args['id']}"
    print("./user/" + index + ".txt")
    if os.path.exists("./user/" + index + ".txt") == True:
        file = open("./user/" + index + ".txt", 'x')
        file.write(name['nom'] + "\n" + name['prenom'])
        file.close()
    else:
        name ="ton code fonctionne pas"
    return make_response(name, 200)



@app.route("/del_user", methods=["DELETE"])
def del_user():
    """
    supprimer un user
    params:none
    return: une reponse pisitive/négatif si le user est supprimer


    """

    id = f"{request.args['id']}"
    print("./user/"+id+".txt")

    if os.path.exists("./user/"+id+".txt") == True:
        os.remove("./user/" +id + ".txt")
        delete = "Le user " + id + " à été supprimer"
    else:
        delete = "le user n'existait pas"

    return make_response(delete,200)



"""
crée un fichier .txt avec un nouvelle utilisateur
params: newUser(un json avec le nom et le prenom d'un nouvel utilisateur)
return: soit le json si tout a fonctionner soit un message d'erreur
"""


@app.route("/adduser", methods=["POST"])
def add_user():
    json = request.get_json()
    index = f"{request.args['id']}"
    if os.path.exists("./user/" + index + ".txt") == False:
        file = open("./user/" + index + ".txt", 'x')
        file.write(json['nom'] + "\n" + json['prenom'])
        file.close()
        name = "l'utilisateur est bien enregistrer"
    else:
        name = "l'utilisateur existe deja"
    return make_response(name, 200)


if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=8081,
        debug=True,
    )


