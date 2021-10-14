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
#@app.route("/", methods=["GET"])
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
    #collection.insert(json)

    name = f"arguments : {request.args['name']}"

    jsso_name = {"name": name}
    #make_response(jsso_name, 200)
    champion = collection.find({"name" : name})
    all_champ = []
    for item in champion:
        all_champ.append(item)

    if len(all_champ) == 0:

        collection.insert(json)

        response = "Le champion est bien enregistré.\n" + name
    else:
        response = "Ce champion existe déjà : " + name

    return make_response(response, 200)


"""
    modifer un Champion
    params: Champion (un json avec les information du champion)
    return : le json modifer
"""
@app.route("/modifyChampion", methods=["PATCH"])
def patch_user():
    json = request.get_json()
    index = f"{request.args['name']}"

    champion = collection.find({"name":index})

    all_champ = []
    for item in champion:
        all_champ.append(item)
        print(len(all_champ))
    if len(all_champ) > 0:

        collection.find_one_and_replace({"name" : index}, json)

        response = "Le champion à bien été mise à jour."
    else:
        response = "Le champion n'existe pas. Création du champion?"
    return make_response(response, 200)






    """
        ajouter un Champion
        params: Champion (un json avec les information du champion)
        return : le json ajouté
    """







if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=8081,
        debug=True,
    )
