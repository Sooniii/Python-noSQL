from flask import Flask
from flask import request
from flask import make_response

import pymongo
import champion
import joueur
import item
app = Flask(__name__)

client = pymongo.MongoClient(
    "mongodb+srv://m001-student:root@cluster0.oia9n.mongodb.net/Lol?retryWrites=true&w=majority")

collection_player = db.Player

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


@app.route("/joueur", methods=["GET"])
def get_joueur():
    return joueur.displayPlayer()

@app.route("/modifyJoueur", methods=["PATCH"])
def modify_joueur():
    return joueur.patch_player()

@app.route("/deleteJoueur", methods=["DELETE"])
def delete_joueur():
    return joueur.delete_joueur()


@app.route("/item", methods=["GET"])
def get_item():
    return item.displayItem()

@app.route("/modifyItem", methods=["PATCH"])
def modify_item():
    return item.patch_item()

@app.route("/deleteItem", methods=["DELETE"])
def delete_item():
    return item.delete_Item()




if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=8081,
        debug=True,
    )

