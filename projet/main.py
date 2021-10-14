from flask import Flask
from flask import request
from flask import make_response
import pymongo

app = Flask(__name__)

client = pymongo.MongoClient(
    "mongodb+srv://m001-student:root@cluster0.oia9n.mongodb.net/Lol?retryWrites=true&w=majority")
db = client.Lol
collection = db.Champion

"""
Affiche la liste des champions en fonction de criteres de recherches
params: none
return: la liste des champions (String)

"""
@app.route("/", methods=["GET"])
def display():



    if "name" in request.args:
        index = f"{request.args['name']}"
        champion = collection.find({"name": str(index)})
    elif "title" in request.args:
        index = f"{request.args['title']}"
        champion = collection.find({"title": str(index)})
    elif "class" in request.args:
        index = f"{request.args['class']}"
        champion = collection.find({"class": str(index)})
    elif "role" in request.args:
        index = f"{request.args['role']}"
        champion = collection.find({"role": str(index)})
    else:
        champion = collection.find()

    all_champ = ""
    for item in champion:
        all_champ =  all_champ + "<p>" + item['name'] + "</p>"




    return make_response(all_champ)
"""
fonction cherchant  adelete les champion 
param : nom des champions 
return un message nous disant que la suppression a eu lieu 
"""

@app.route("/delete", methods=["DELETE"])
def delete():
    result= ""
    index = f"{request.args['name']}"
    champion = collection.find()
    validation = False
    for item in champion:
        if index == item['name'] :
            validation = True

    if validation == True:
        result = collection.delete_one({"name": index})
        response = "Le champion à bien été supprimer.\n"
    else:
        response = "le champion choisi a déjà été supprimer ou n'exise pas"





    return make_response(response, 200)


"""
    ajouter un Champion
    params: Champion (un json avec les information du champion)
    return : le json ajouté
"""
@app.route("/addChampion", methods=["POST"])
def add():
    json = request.get_json()
    name = json["name"]
    champion = collection.find()
    exist = False
    for item in champion:
        if name == item['name']:
            exist = True
    if exist == False:
        collection.insert(json)
        response = "Le champion est bien enregistré : " + json["name"]
    else:
        response = "Ce champion existe déjà : " + json["name"]
    return make_response(response, 200)


if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=8081,
        debug=True,
    )








"""
    modifer un Champion
    params: Champion (un json avec les information du champion)
    return : le json modifer
"""
@app.route("/modifyChampion", methods=["PATCH"])
def patch_user():
    name = request.get_json()
    index = f"{request.args['id']}"
    if collection.find({"_id" : index}) == True:

        collection.updateMany({"_id" : index}, { json })

        response = "Le champion à bien été mise à jour.\n" + json
    else:
        response = "Le champion n'existe pas. Création du champion.\n" + json
    return make_response(name, 200)

