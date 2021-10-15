from flask import Flask
from flask import request
from flask import make_response

import pymongo

client = pymongo.MongoClient(
    "mongodb+srv://m001-student:root@cluster0.oia9n.mongodb.net/Lol?retryWrites=true&w=majority")

db = client.Lol
collection_champion = db.Champion


"""
Affiche la liste des champions en fonction de criteres de recherches
params: none
return: la liste des champions (String)

"""
def display_champion():


    if "name" in request.args:
        index = f"{request.args['name']}"
        champion = collection_champion.find({"name": str(index)})
    elif "title" in request.args:
        index = f"{request.args['title']}"
        champion = collection_champion.find({"title": str(index)})
    elif "class" in request.args:
        index = f"{request.args['class']}"
        champion = collection_champion.find({"class": str(index)})
    elif "role" in request.args:
        index = f"{request.args['role']}"
        champion = collection_champion.find({"role": str(index)})
    else:
        champion = collection_champion.find()
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
def delete_champion():
    result= ""
    index = f"{request.args['name']}"
    champion = collection_champion.find()
    validation = False
    for item in champion:
        if index == item['name'] :
            validation = True

    if validation == True:
        result = collection_champion.delete_one({"name": index})
        response = "Le champion à bien été supprimer.\n"
    else:
        response = "le champion choisi a déjà été supprimer ou n'exise pas"

    return make_response(response, 200)

"""
    ajouter un Champion
    params: Champion (un json avec les information du champion)
    return : le json ajouté
"""

def add_champion():
    json = request.get_json()
    name = json["name"]
    champion = collection_champion.find({"name":name})
    all_champ = []

    for item in champion:
        all_champ.append(item)
    if not all_champ:
        collection_champion.insert(json)
        response = "Le champion est bien enregistré : " + json["name"]
    else:
        response = "Ce champion existe déjà : " + json["name"]
    return make_response(response, 200)

"""
    modifer un Champion
    params: Champion (un json avec les information du champion)
    return : le json modifer
"""

def patch_champion():
    json = request.get_json()
    index = f"{request.args['name']}"

    champion = collection_champion.find({"name":index})

    all_champ = []
    for item in champion:
        all_champ.append(item)
        print(len(all_champ))
    if len(all_champ) > 0:

        collection_champion.find_one_and_replace({"name" : index}, json)

        response = "Le champion à bien été mise à jour."
    else:
        response = "Le champion n'existe pas. Création du champion?"
    return make_response(response, 200)


