
from flask import Flask
from flask import request
from flask import make_response
import pymongo

app = Flask(__name__)


client = pymongo.MongoClient("mongodb+srv://m001-student:root@cluster0.oia9n.mongodb.net/Lol?retryWrites=true&w=majority")
db = client.Lol
collection = db.Champion



@app.route("/", methods=["GET","POST"])
def display():
    return(str(collection.find_one()))


if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=8081,
        debug=True,
    )



"""
    modifer un Champion
    params: Champion (un json avec les information du champion)
    return : le json ajouté
"""
@app.route("/addChampion", methods=["POST"])
def add():
    json = request.get_json()
    index = f"{request.args['id']}"
    if collection.find({"_id" : index}) == False:

        collection.insert(json)

        response = "Le champion est bien enregistrer.\n" + json
    else:
        response = "Un champion existe déjà.\n" + collection.find({"_id" : index})

    return make_response(response, 200)




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

