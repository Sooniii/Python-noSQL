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
    ajouter un Champion
    params: Champion (un json avec les information du champion)
    return : le json ajouté
"""
@app.route("/addChampion", methods=["POST"])
def add():
    json = request.get_json()
    name = json["name"]
    champion = collection.find()
    for item in champion:
        item['name']
        print(name)
        print(item['name'])
        if name == item['name']:

            collection.insert(json)

            response = "Le champion est bien enregistré.\n" + json["name"]
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

