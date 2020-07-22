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


@app.route('/edit_mod/<mod_id>')
def edit_mod(mod_id):
    the_mod = mongo.db.mods.find_one({"_id": ObjectId(mod_id)})
    all_categories = mongo.db.categories.find()
    return render_template('editmod.html', mod=the_mod, categories=all_categories)


@app.route('/update_mod/<mod_id>', methods=["POST"])
def update_mod(mod_id):
    mods = mongo.db.mods
    mods.update({'_id': ObjectId(mod_id)},
                 {
        'mod_name': request.form.get('mod_name'),
        'category_name': request.form.get('category_name'),
        'mod_description': request.form.get('mod_description'),
        'mod_link': request.form.get('mod_link'),
        'is_must_have': request.form.get('is_must_have')
    })
    return redirect(url_for('get_mods'))


@app.route('/delete_mod/<mod_id>')
def delete_mod(mod_id):
    mongo.db.mods.remove({'_id': ObjectId(mod_id)})
    return redirect(url_for('get_mods'))


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
