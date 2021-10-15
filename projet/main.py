from flask import Flask
from flask import request
from flask import make_response

import pymongo
import champion
import joueur
import item
app = Flask(__name__)


#
# Apelle des fonctions poour la collection: champion
#
@app.route("/champion", methods=["GET"])
def get_champion():
    return champion.display_champion()

@app.route("/deleteChampion", methods=["DELETE"])
def supp_champion():
    return champion.delete_champion()

@app.route("/addChampion", methods=["POST"])
def add_champion():
    return champion.add_champion()

@app.route("/modifyChampion", methods=["PATCH"])
def modify_champion():
    return champion.patch_champion()

#
# Apelle des fonctions poour la collection: joueur
#
@app.route("/joueur", methods=["GET"])
def get_joueur():
    return joueur.displayPlayer()

@app.route("/modifyJoueur", methods=["PATCH"])
def modify_joueur():
    return joueur.patch_player()

@app.route("/deleteJoueur", methods=["DELETE"])
def delete_joueur():
    return joueur.delete_joueur()

@app.route("/addJoueur", methods=["POST"])
def add_Joueur():
    return joueur.add_player()

#
# Apelle des fonctions poour la collection: item
#
@app.route("/item", methods=["GET"])
def get_item():
    return item.displayItem()

@app.route("/modifyItem", methods=["PATCH"])
def modify_item():
    return item.patch_item()

@app.route("/deleteItem", methods=["DELETE"])
def delete_item():
    return item.delete_Item()

@app.route("/addItem", methods=["POST"])
def add_item():
    return item.add_item()



if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=8081,
        debug=True,
    )

