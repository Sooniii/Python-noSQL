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
    return make_response(reponse,200)
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





if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=8081,
        debug=True,
    )

