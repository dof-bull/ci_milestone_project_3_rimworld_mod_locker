import os
from flask import Flask, render_template, redirect, request, url_for, session
import bcrypt
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from os import path
if path.exists("env.py"):
    import env

app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.getenv('MONGO_DBNAME')
app.config["MONGO_URI"] = os.getenv('MONGO_URI', 'mongodb://localhost')

mongo = PyMongo(app)


@app.route('/')
@app.route('/browse_mods')
def browse_mods():
    '''Returns all category types & returns all mods in database'''
    return render_template(
        "mods.html",
        mods=mongo.db.mods.find().sort("mod_name"),
        categories=mongo.db.categories.find().sort("category_name"),
        page_title="Browse Mods"
        )


@app.route('/browse_mods/filter', methods=['POST'])
def filter():
    '''Returns selected category type & returns mods of the selected type'''
    filtermods = mongo.db.mods.find(
        {'category_name': request.form.get('category_name')})
    return render_template(
        "filter.html",
        filtermods=filtermods,
        categories=mongo.db.categories.find().sort("category_name"),
        category_selected=request.form.get('category_name'),
        page_title="Browse Mods"
        )


@app.route('/about')
def about():
    '''Renders the about page'''
    return render_template(
        "about.html",
        page_title="About"
        )


@app.route('/add_mod')
def add_mod():
    '''Provides form to add a mod'''
    return render_template(
        'addmod.html',
        categories=mongo.db.categories.find().sort("category_name"),
        page_title="Add Mod"
        )


@app.route('/insert_mod', methods=['POST'])
def insert_mod():
    '''Takes form input data & inserts into db'''
    mods = mongo.db.mods
    mods.insert_one(request.form.to_dict())
    return redirect(
        url_for('browse_mods')
        )


@app.route('/edit_mod/<mod_id>')
def edit_mod(mod_id):
    '''Takes data from db to autofill form'''
    the_mod = mongo.db.mods.find_one({"_id": ObjectId(mod_id)})
    all_categories = mongo.db.categories.find().sort("category_name")
    return render_template(
        'editmod.html',
        mod=the_mod,
        categories=all_categories,
        page_title="Edit Mods"
        )


@app.route('/update_mod/<mod_id>', methods=["POST"])
def update_mod(mod_id):
    '''Takes form input data and updates existing data'''
    mods = mongo.db.mods
    mods.update({'_id': ObjectId(mod_id)}, {
        'mod_name': request.form.get('mod_name'),
        'category_name': request.form.get('category_name'),
        'mod_description': request.form.get('mod_description'),
        'mod_link': request.form.get('mod_link'),
        'is_must_have': request.form.get('is_must_have')
    })
    return redirect(
        url_for('browse_mods')
        )


@app.route('/delete_mod/<mod_id>')
def delete_mod(mod_id):
    '''Deletes selected mod data from database'''
    mongo.db.mods.remove({'_id': ObjectId(mod_id)})
    return redirect(
        url_for('browse_mods')
        )


@app.route('/get_categories')
def get_categories():
    '''Returns all category in database'''
    return render_template(
        'categories.html',
        categories=mongo.db.categories.find().sort("category_name"),
        page_title="Manage Catergories"
        )


@app.route('/add_category')
def add_category():
    '''Provides form to add a category'''
    return render_template(
        'addcategory.html',
        page_title="Add Category"
        )


@app.route('/insert_category', methods=['POST'])
def insert_category():
    '''Takes form input data & inserts into db'''
    category_doc = {'category_name': request.form.get('category_name')}
    mongo.db.categories.insert_one(category_doc)
    return redirect(
        url_for('get_categories')
        )


@app.route('/edit_category/<category_id>')
def edit_category(category_id):
    '''Takes data from db to autofill form'''
    return render_template(
        'editcategory.html',
        category=mongo.db.categories.find_one({'_id': ObjectId(category_id)}),
        page_title="Edit Category"
        )


@app.route('/update_category/<category_id>', methods=['POST'])
def update_category(category_id):
    '''Takes form input data and updates existing category data'''
    mongo.db.categories.update(
        {'_id': ObjectId(category_id)},
        {'category_name': request.form.get('category_name')})
    return redirect(
        url_for('get_categories')
        )


@app.route('/delete_category/<category_id>')
def delete_category(category_id):
    '''Deletes selected category data from database'''
    mongo.db.categories.remove({'_id': ObjectId(category_id)})
    return redirect(
        url_for('get_categories')
        )


# User Login - based on tutorial from Pretty Printed


@app.route('/signIn')
def signIn():
    '''Detects if user is signed in already'''
    if 'username' in session:
        return 'You are logged in as ' + session['username']

    return render_template(
        'signIn.html',
        page_title="Login"
        )


@app.route('/login', methods=["POST"])
def login():
    '''Allows user to log in if using correct username & password'''
    users = mongo.db.users
    login_user = users.find_one({'name': request.form['username']})
    if login_user:
        if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_user['password']) == login_user['password']:
            session['username'] = request.form['username']
            return redirect(
                url_for('signIn')
                )
        return 'Invalid username/password combination'

    return 'Invalid username/password combination'


@app.route('/register', methods=["POST", "GET"])
def register():
    '''Allows a user to create a new user id and passowrd'''
    if request.method == "POST":
        users = mongo.db.users
        existing_user = users.find_one({'name': request.form['username']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(
                request.form['pass'].encode('utf-8'), bcrypt.gensalt())
            users.insert(
                {'name': request. form['username'], 'password': hashpass})
            session['username'] = request.form['username']
            return redirect(
                url_for('signIn')
                )

        return 'That username already exists'

    return render_template(
        'register.html',
        page_title="Register"
        )


if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
