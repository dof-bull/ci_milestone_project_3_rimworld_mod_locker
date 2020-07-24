import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from os import path
if path.exists("env.py"):
    import env

app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.getenv('MONGO_DBNAME')
app.config["MONGO_URI"] = os.getenv('MONGO_URI', 'mongodb://localhost')

mongo = PyMongo(app)


# Browse Mod Page


@app.route('/')
@app.route('/browse_mods')
def browse_mods():
    return render_template(
                            "mods.html", mods=mongo.db.mods.find(
                                 ).sort("mod_name"),
                            categories=mongo.db.categories.find(
                            ).sort("category_name"), category="Animals",
                            page_title="Browse Mods")


# Filter on Browse Mod Page


@app.route('/filter_categories', methods=['POST'])
def filter_categories():
    mods = mongo.db.mods
    mods.insert_one(request.form.to_dict())
    return redirect(url_for('browse_mods'))

# About Page


@app.route('/about')
def about():
    return render_template("about.html", page_title="About")


# Add Mod


@app.route('/add_mod')
def add_mod():
    return render_template(
        'addmod.html', categories=mongo.db.categories.find().sort(
            "category_name"), page_title="Add Mod"
        )


@app.route('/insert_mod', methods=['POST'])
def insert_mod():
    mods = mongo.db.mods
    mods.insert_one(request.form.to_dict())
    return redirect(url_for('browse_mods'))


# Edit Mod


@app.route('/edit_mod/<mod_id>')
def edit_mod(mod_id):
    the_mod = mongo.db.mods.find_one({"_id": ObjectId(mod_id)})
    all_categories = mongo.db.categories.find().sort("category_name")
    return render_template(
                            'editmod.html', mod=the_mod,
                            categories=all_categories, page_title="Edit Mods"
)


@app.route('/update_mod/<mod_id>', methods=["POST"])
def update_mod(mod_id):
    mods = mongo.db.mods
    mods.update({'_id': ObjectId(mod_id)}, {
        'mod_name': request.form.get('mod_name'),
        'category_name': request.form.get('category_name'),
        'mod_description': request.form.get('mod_description'),
        'mod_link': request.form.get('mod_link'),
        'is_must_have': request.form.get('is_must_have')
    })
    return redirect(url_for('browse_mods'))


# Delete Mod


@app.route('/delete_mod/<mod_id>')
def delete_mod(mod_id):
    mongo.db.mods.remove({'_id': ObjectId(mod_id)})
    return redirect(url_for('browse_mods'))


# Categories Page


@app.route('/get_categories')
def get_categories():
    return render_template('categories.html',
                           categories=mongo.db.categories.find().sort(
                               "category_name"), page_title="Manage Catergories")


# Add Category


@app.route('/add_category')
def add_category():
    return render_template('addcategory.html', page_title="Add Category")


@app.route('/insert_category', methods=['POST'])
def insert_category():
    category_doc = {'category_name': request.form.get('category_name')}
    mongo.db.categories.insert_one(category_doc)
    return redirect(url_for('get_categories'))


# Edit Category


@app.route('/edit_category/<category_id>')
def edit_category(category_id):
    return render_template('editcategory.html',
                           category=mongo.db.categories.find_one(
                               {'_id': ObjectId(category_id)}), page_title="Edit Category")


@app.route('/update_category/<category_id>', methods=['POST'])
def update_category(category_id):
    mongo.db.categories.update(
        {'_id': ObjectId(category_id)},
        {'category_name': request.form.get('category_name')})
    return redirect(url_for('get_categories'))


# Delete Category


@app.route('/delete_category/<category_id>')
def delete_category(category_id):
    mongo.db.categories.remove({'_id': ObjectId(category_id)})
    return redirect(url_for('get_categories'))


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
