
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
