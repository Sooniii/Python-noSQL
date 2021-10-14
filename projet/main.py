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
    reponse = ""
    all_champ = []

    for item in champion:
        all_champ.append(item)

    if not all_champ:
        reponse = "Aucun champion ne correspond a votre recherche"
        return make_response(reponse)

    #
    # Pagination
    #
    if "page" in request.args:
        # on recupere l'index de la pahge et on la passe en int
        index = f"{request.args['page']}"
        if str.isdigit(index):
            index = int(index)
        else:
            reponse = "La page selectionner n'est pas valide"
            return make_response(reponse)
        #
        # On verifie qu'on ne demande pas plus de champions que il y en a
        #
        if len(all_champ) <= index * 5 - 1:
            # Si oui, lors de la concatenation, on n'indique pas la derniere position
            concenat_champ = all_champ[index * 5 - 5:]
        else:
            # Si non on ne prend que 5 champions
            concenat_champ = all_champ[index * 5 - 5: index * 5]

        # construction des reponse
        for item in concenat_champ:
            reponse = reponse + "<p>" + item['name'] +" | "+item['title'] +"</p>"
    else:
        for item in all_champ:
            reponse = reponse + "<p>" + item['name'] +" | "+item['title'] +" | "+str(item['class']) +" | "+ str(item['role']) + "</p>"

    return make_response(reponse)


"""
    modifer un Champion
    params: Champion (un json avec les information du champion)
    return : le json ajouté
"""


@app.route("/addChampion", methods=["POST"])
def add():
    json = request.get_json()
    index = f"{request.args['id']}"
    if collection.find({"_id": index}) == False:

        collection.insert(json)

        response = "Le champion est bien enregistrer.\n"
    else:
        test = collection.find({"_id": index})
        print(test['name'])
        response = "Un champion existe déjà.\n"  # + collection.find({"_id" : index})

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
    if collection.find({"_id": index}) == True:

        collection.updateMany({"_id": index}, {json})

        response = "Le champion à bien été mise à jour.\n" + json
    else:
        response = "Le champion n'existe pas. Création du champion.\n" + json
    return make_response(name, 200)
