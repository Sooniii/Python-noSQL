from flask import Flask
from flask import request
from flask import make_response
import pymongo

client = pymongo.MongoClient(
    "mongodb+srv://m001-student:root@cluster0.oia9n.mongodb.net/Lol?retryWrites=true&w=majority")
db = client.Lol
collection_player = db.Player

"""
Affiche la liste des joueur en fonction de criteres de recherches
params: none
return: la liste des joueur (String)

"""



def displayPlayer():


    if "name" in request.args:
        index = f"{request.args['name']}"
        joueur = collection_player.find({"name": str(index)})
    elif "title" in request.args:
        index = f"{request.args['equipe']}"
        joueur = collection_player.find({"equipe": str(index)})
    elif "role" in request.args:
        index = f"{request.args['role']}"
        joueur = collection_player.find({"role": str(index)})
    else:
        joueur = collection_player.find()
    reponse = ""
    all_player = []

    for item in joueur:

        all_player.append(item)

    if not all_player:
        reponse = "Aucun joueur ne correspond a votre recherche"
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
        if len(all_player) <= index * 5 - 1:
            # Si oui, lors de la concatenation, on n'indique pas la derniere position
            concenat_player = all_player[index * 5 - 5:]
        else:
            # Si non on ne prend que 5 champions
            concenat_player = all_player[index * 5 - 5: index * 5]

        # construction des reponse
        for item in concenat_player:
            reponse = reponse + "<p>" + item['name'] +" | "+item['title'] +"</p>"
    else:
        for item in all_player:
            reponse = reponse + "<p>" + item['name'] +" | "+item['equipe'] +" | "+str(item['role']) + "</p>"
    return make_response(reponse,200)



"""
    modifer un Joueur
    params: Joueur (un json avec les information du joueur)
    return : le json modifer
"""

def patch_player():
    json = request.get_json()
    index = f"{request.args['name']}"

    joueur = collection_player.find({"name":index})

    all_player = []
    for item in joueur:
        all_player.append(item)
        print(len(all_player))
    if len(all_player) > 0:

        collection_player.find_one_and_replace({"name" : index}, json)

        response = "Le joueur à bien été mise à jour."
    else:
        response = "Le joueur n'existe pas. Création du joueur?"
    return make_response(response, 200)

"""
fonction cherchant a delete les joueur 
param : nom des joueur 
return un message nous disant que la suppression a eu lieu 
"""

@app.route("/deleteJoueur", methods=["DELETE"])
def delete_joueur():
    result= ""
    index = f"{request.args['name']}"
    joueur = collection_player.find()
    validation = False
    for item in joueur:
        if index == item['name'] :
            validation = True

    if validation == True:
        result = collection_player.delete_one({"name": index})
        response = "Le joueur à bien été supprimer.\n"
    else:
        response = "le joueur choisi a déjà été supprimer ou n'exise pas"

    return make_response(response, 200)
