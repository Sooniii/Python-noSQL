from flask import Flask
from flask import request
from flask import make_response

import pymongo


client = pymongo.MongoClient(
    "mongodb+srv://m001-student:root@cluster0.oia9n.mongodb.net/Lol?retryWrites=true&w=majority")
db = client.Lol

collection_item = db.Item

"""
Affiche la liste des objet en fonction de criteres de recherches
params: none
return: la liste des objet (String)

"""


def displayItem():


    if "name" in request.args:
        index = f"{request.args['name']}"
        objet = collection_item.find({"name": str(index)})
    elif "effet" in request.args:
        index = f"{request.args['effet']}"
        objet = collection_item.find({"effet": str(index)})
    elif "prix" in request.args:
        index = f"{request.args['prix']}"
        objet = collection_item.find({"prix": str(index)})
    else:
        objet = collection_item.find()
    reponse = ""
    all_item = []

    for item in objet:

        all_item.append(item)

    if not all_item:
        reponse = "Aucun item ne correspond a votre recherche"
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
        if len(all_item) <= index * 5 - 1:
            # Si oui, lors de la concatenation, on n'indique pas la derniere position
            concenat_item = all_item[index * 5 - 5:]
        else:
            # Si non on ne prend que 5 champions
            concenat_item = all_item[index * 5 - 5: index * 5]

        # construction des reponse
        for item in concenat_item:
            reponse = reponse + "<p>" + item['name'] +" | "+item['effet'] +"</p>"
    else:
        for item in all_item:
            reponse = reponse + "<p>" + item['name'] +" | "+item['effet'] +" | "+str(item['prix']) + "</p>"
    return make_response(reponse,200)

"""
    modifer un item
    params: Objet (un json avec les information du objet)
    return : le json modifer
"""

def patch_item():
    json = request.get_json()
    index = f"{request.args['name']}"

    objet = collection_item.find({"name":index})

    all_item = []
    for item in objet:
        all_item.append(item)
        print(len(all_item))
    if len(all_item) > 0:

        collection_item.find_one_and_replace({"name" : index}, json)

        response = "L'objet à bien été mise à jour."
    else:
        response = "L'objet n'existe pas. Création de l'objet?"
    return make_response(response, 200)

"""
fonction cherchant a delete les objet 
param : nom des objets 
return un message nous disant que la suppression a eu lieu 
"""


def delete_Item():
    result= ""
    index = f"{request.args['name']}"
    objet = collection_item.find()
    validation = False
    for item in objet:
        if index == item['name'] :
            validation = True

    if validation == True:
        result = collection_item.delete_one({"name": index})
        response = "L'objet à bien été supprimer.\n"
    else:
        response = "l'objet choisi a déjà été supprimer ou n'exise pas"

    return make_response(response, 200)

"""
    ajouter un objet
    params: objet (un json avec les information du champion)
    return : le json ajouté
"""

def add_item():
    json = request.get_json()
    name = json["name"]
    objet = collection_item.find({"name":name})
    all_item = []

    for item in objet:
        all_item.append(item)
    if not all_item:
        collection_champion.insert(json)
        response = "L'objet est bien enregistré : " + json["name"]
    else:
        response = "Cet objet existe déjà : " + json["name"]
    return make_response(response, 200)