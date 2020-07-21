import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from os import path
if path.exists("env.py"):
  import env

app = Flask(__name__)

app.config["MONGO_DBNAME"] = 'rimworld_mod_locker'
app.config["MONGO_URI"] = os.getenv('MONGO_URI', 'mongodb://localhost')

mongo = PyMongo(app)


@app.route('/')
@app.route('/get_mods')
def get_mods():
    return render_template("mods.html", mods=mongo.db.mods.find())


@app.route('/add_mod')
def add_mod():
    return render_template('addmod.html', categories=mongo.db.categories.find())


@app.route('/insert_mod', methods=['POST'])
def insert_mod():
    mods = mongo.db.mods
    mods.insert_one(request.form.to_dict())
    return redirect(url_for('get_mods'))


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
