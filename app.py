import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId 

app = Flask(__name__)

app.config["MONGO_DBNAME"] = 'rimworld_mod_locker'
app.config["MONGO_URI"] = 'mongodb+srv://dbUser:Iwant3mods@cluster0.aadrh.mongodb.net/rimworld_mod_locker?retryWrites=true&w=majority'

mongo = PyMongo(app)

@app.route('/')
@app.route('/get_mods')
def get_mods():
    return render_template("mods.html", mods=mongo.db.mods.find())


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
