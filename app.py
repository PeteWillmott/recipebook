from flask import Flask, render_template, redirect, request, url_for, flash, session, g
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import os
import pymongo

app = Flask(__name__)

app.config["MONGO_DBNAME"] = 'project'
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

mongo = PyMongo(app)

# collections

recipe_coll = mongo.db.recipe
users_coll = mongo.db.users

# globals

allergens = ['gluten', 'dairy', 'eggs', 'sea food', 'nuts', 'alliums']
types = ['breakfast', 'snack', 'main meal', 'dessert', 'baking']
categories = ['vegetarian', 'vegan']


def hrs_to_mins(time_hrs):

    """Converts time in hours into time in minutes."""
    if time_hrs:
        time_mins = int(time_hrs) * 60
    else:
        time_mins = 0
    return time_mins


def is_admin(f):
    @wraps(f)
    def admin_test(*args, **kwargs):

        """Access control check for admin users."""
        if not g.admin:
            flash("You must be an Admin to access these functions.")

            return redirect(url_for("index"))

        return f(*args, **kwargs)

    return admin_test


def is_user(f):
    @wraps(f)
    def user_test(*args, **kwargs):

        """Access control check for users."""
        if not g.user:
            flash("You must be logged in to access these functions.")

            return redirect(url_for("index"))

        return f(*args, **kwargs)

    return user_test

# routes


@app.route('/')
def index():

    """Home page."""
    votes = recipe_coll.find({"authorisation": "allowed"}).sort("votes", pymongo.DESCENDING).limit(4)

    return render_template("index.html", votes=votes)


@app.before_request
def before_request():

    """Sets global user for access control."""
    g.user = None
    g.name = None
    g.admin = None
    if 'email' and 'user' in session:
        g.user = session['email']
        g.name = session['user']
    if 'type' in session:
        if session['type'] == "admin":
            g.admin = "admin"


@app.route('/register', methods=['GET', 'POST'])
def register():

    """User registration function."""
    if request.method == 'POST':
        email = users_coll.find_one({"email": request.form.get('email')})
        if email:
            flash("An account for {} already exists, please log in".format
                  (request.form["email"]))
            return redirect(url_for('index'))

        if request.form.get('psswd1') == request.form.get('psswd2'):
            password = generate_password_hash(request.form.get('psswd1'))
            users_coll.insert_one({
                "email": request.form.get('email'),
                "username": request.form.get('username'),
                "password": password,
                "admin": False})
            session['user'] = request.form.get('username')
            session['email'] = request.form.get('email')

            return redirect(url_for("index"))

        else:
            flash("The passwords must match")

    return render_template("register.html")


@app.route('/login', methods=['GET', 'POST'])
def login():

    """Log in function, adds the user/admin to the session."""
    if request.form.get('email') and request.form.get('password'):
        login = users_coll.find_one(
            {'email': request.form.get('email')})
        if check_password_hash(login['password'], request.form.get('password')):
            session['user'] = login['username']
            session['email'] = login['email']
            if login['admin']:
                session['type'] = "admin"
                recipes = recipe_coll.find({"authorisation": "not"})

                return redirect(url_for("admin", recipes=recipes))

    return_url = request.referrer or '/'

    return redirect(return_url)


@app.route('/logout', methods=['POST'])
@is_user
def logout():

    """Log out function, clears the user from the session."""
    session.pop('user', None)
    session.pop('type', None)
    g.user = None
    g.admin = None

    return_url = request.referrer or '/'

    return redirect(return_url)


@app.route('/search', methods=['GET', 'POST'])
def search():

    """Search function, multi-critera search."""
    ingredients = []
    ingredient_list = recipe_coll.distinct("ingredients")
    for ing in ingredient_list:
        ingredient = ing.split(",")
        ingredients.append(ingredient[0])
    ingredients = list(dict.fromkeys(ingredients))

    return render_template(
                            "search.html", ingredients=ingredients,
                            allergens=allergens, types=types,
                            categories=categories)


@app.route('/searchresults', methods=['GET', 'POST'])
def search_results():

    """Displays search form output."""
    allergen_list = []
    type_list = []
    form_data = request.form
    ingredient = False
    recipe_type = False
    category = request.form.get("category")

    if category == "vegan":
        cat_list = ["vegan"]
    elif category == "vegetarian":
        cat_list = ["vegetarian", "vegan"]
    else:
        cat_list = ["vegetarian", "vegan", "omni"]

    for key in form_data:
        if 'allergen' in key:
            allergen_list.append(form_data[key])
    for key in form_data:
        if 'type'in key:
            type_list.append(form_data[key])
            recipe_type = True

    ing = request.form.get('ingredient')
    if ing is None:
        ingredient = '^/.'
    else:
        ingredient = ing
    spicyness = request.form.get('spicyness', type=int)
    if spicyness is None:
        spicyness = {'$lte': 3}
    difficulty = request.form.get('difficulty', type=int)
    if difficulty is None:
        difficulty = {'$lte': 3}
    time = request.form.get('time', type=int)

    if recipe_type is True:
        recipes = recipe_coll.find(
            {"authorisation": "allowed",
             "ingredients": {'$regex': ingredient},
             "type": {'$in': type_list},
             "category": {'$in': cat_list},
             "allergens": {'$nin': allergen_list},
             "spicyness": spicyness,
             "difficulty": difficulty,
             "total_time": {'$lte': time}})
    else:
        recipes = recipe_coll.find(
            {"authorisation": "allowed",
             "ingredients": {'$regex': ingredient},
             "category": {'$in': cat_list},
             "allergens": {'$nin': allergen_list},
             "spicyness": spicyness,
             "difficulty": difficulty,
             "total_time": {'$lte': time}})

    return render_template("searchresults.html", recipes=recipes, recipe_type=recipe_type, cat_list=cat_list, allergen_list=allergen_list, type_list=type_list)


@app.route('/browse', methods=['GET', 'POST'])
def browse():

    """Display the recipes on individual cards."""
    recipes = recipe_coll.find({"authorisation": "allowed"})
    if g.user:
        user = users_coll.find_one({'email': g.user})

        return render_template("browse.html", user=user, recipes=recipes)

    return render_template("browse.html", recipes=recipes)


@app.route('/recipe/<recipe_id>')
def recipe(recipe_id):

    """Display the selected recipe."""
    the_recipe = recipe_coll.find_one({"_id": ObjectId(recipe_id)})
    the_user = users_coll.find_one({'email': g.user})

    return render_template('recipe.html', recipe=the_recipe, user=the_user)


@app.route('/vote', methods=['POST'])
@is_user
def vote():

    """Add a like to the recipe, note user id to disallow multiple likes."""
    if request.method == 'POST':
        recipeID = request.form.get('recipeID')
        votes = request.form.get('votes')
        vote_total = int(votes) + 1
        voted_check = users_coll.find_one({
            'email': g.user,
            'voted': ObjectId(recipeID)})
        if voted_check:
            flash("You have already liked this recipe.")

            return redirect(url_for('recipe', recipe_id=recipeID))

        else:
            recipe_coll.update(
                {"_id": ObjectId(recipeID)}, {'$set': {'votes': vote_total}})
            users_coll.update(
                {'email': g.user}, {'$push': {'voted': ObjectId(recipeID)}})

    return redirect(url_for('recipe', recipe_id=recipeID))


@app.route('/add_favourite', methods=['POST'])
@is_user
def add_favourite():

    """Add a recipe as a favourite."""
    if request.method == 'POST':
        recipeID = request.form.get('recipeID')
        users_coll.update(
            {'email': g.user}, {'$push': {'favourites': recipeID}})

    return redirect(url_for('recipe', recipe_id=recipeID))


@app.route('/favourites')
@is_user
def display_favourites():

    """List preset favourites, with link."""
    user = users_coll.find_one({'email': g.user})
    recipes = recipe_coll.find({"authorisation": "allowed"})

    return render_template("favourites.html", user=user, recipes=recipes)


@app.route('/addnote/<recipe_id>', methods=['GET', 'POST'])
@is_user
def add_note(recipe_id):

    """Annotates the recipe with user entered text."""
    the_recipe = recipe_coll.find_one({"_id": ObjectId(recipe_id)})
    the_user = users_coll.find_one({'email': g.user})
    rcode = the_recipe["recipe_code"]

    if request.method == 'POST':
        content = request.form.get('note_content')
        content = str(content)
        users_coll.update(
            {'email': g.user},
            {'$set':
             {rcode: content}})
        the_user = users_coll.find_one({'email': g.user})

        return render_template('recipe.html', recipe=the_recipe, user=the_user)

    return render_template('addnote.html', recipe=the_recipe, user=the_user)


@app.route('/addrecipe', methods=['GET', 'POST'])
@is_user
def add_recipe():

    """Adds a recipe to the database. Member only area, login required."""
    if request.method == 'POST':

        ingredient_list = []
        instruction_list = []
        ingredient_data = request.form.getlist('ingredient')
        instruction_data = request.form.getlist('instruction')
        for value in ingredient_data:
            ingredient_list.append(value)
        for value in instruction_data:
            instruction_list.append(value)

        prep_time1 = request.form.get('prep_time_hrs')
        prep_time2 = request.form.get('prep_time_mins')
        cook_time1 = request.form.get('cook_time_hrs')
        cook_time2 = request.form.get('cook_time_mins')
        prep_time = hrs_to_mins(prep_time1)
        prep_time += int(prep_time2)
        cook_time = hrs_to_mins(cook_time1)
        cook_time += int(cook_time2)
        total_time = prep_time + cook_time

        category = request.form.get('category')
        if category is None:
            category = "omni"

        recipe = request.form.get('recipe')
        rcode = recipe.replace(" ", "")

        recipe_coll.insert_one({
            "recipe": recipe,
            "recipe_code": rcode,
            "prep_time": prep_time,
            "cook_time": cook_time,
            "total_time": total_time,
            "category": category,
            "url": request.form.get('url'),
            "ingredients": ingredient_list,
            "instructions": instruction_list,
            "difficulty": request.form.get('difficulty', type=int),
            "spicyness": request.form.get('spicyness', type=int),
            "authorisation": "not",
            "author": request.form.get('author'),
            "summary": request.form.get('summary'),
            "type": request.form.getlist('type'),
            "allergens": request.form.getlist('allergen'),
            "votes": "0"})
        user = users_coll.find_one({'email': g.user})
        recipes = recipe_coll.find({"authorisation": "allowed"})

        return render_template("browse.html", user=user, recipes=recipes)

    return render_template("addrecipe.html", allergens=allergens, types=types)


@app.route('/editrecipe/<recipe_id>', methods=['GET', 'POST'])
@is_user
def edit_recipe(recipe_id):

    """Displays recipe for editing."""
    recipe = recipe_coll.find_one({"_id": ObjectId(recipe_id)})
    if g.user == recipe['author'] or g.admin:
        if recipe['prep_time'] != 0:
            prep_hrs = recipe['prep_time'] // 60
            prep_mins = recipe['prep_time'] % 60
        else:
            prep_hrs = 0
            prep_mins = 0
        if recipe['cook_time'] != 0:
            cook_hrs = recipe['cook_time'] // 60
            cook_mins = recipe['cook_time'] % 60
        else:
            cook_hrs = 0
            cook_mins = 0
        return render_template("editrecipe.html", recipe=recipe,
                               allergens=allergens, types=types,
                               prep_hrs=prep_hrs, prep_mins=prep_mins,
                               cook_hrs=cook_hrs, cook_mins=cook_mins)

    flash("Only the original author or an admin may edit a recipe.")
    return_url = request.referrer or '/'

    return redirect(return_url)


@app.route('/updaterecipe/<recipe_id>', methods=['GET', 'POST'])
def update_recipe(recipe_id):

    """Updates database with edited recipe."""
    if g.user:
        if request.method == 'POST':
            category = request.form.get('category')
            if category is None:
                category = "omni"

            prep_time1 = request.form.get('prep_time_hrs')
            prep_time2 = request.form.get('prep_time_mins')
            cook_time1 = request.form.get('cook_time_hrs')
            cook_time2 = request.form.get('cook_time_mins')
            prep_time = hrs_to_mins(prep_time1)
            prep_time += int(prep_time2)
            cook_time = hrs_to_mins(cook_time1)
            cook_time += int(cook_time2)
            total_time = prep_time + cook_time

            #recipe_coll.update(
                #{'_id': ObjectId(recipe_id)},
                #{'$push': {"type": [request.form.get('type')]}})
                
            recipe_coll.update(
                {'_id': ObjectId(recipe_id)},
                {'$set': {
                    'category': category,
                    "prep_time": prep_time,
                    "cook_time": cook_time,
                    "total_time": total_time,
                    'recipe': request.form.get('recipe'),
                    'ingredients': request.form.getlist('ingredient'),
                    'url': request.form.get('url'),
                    'summary': request.form.get('summary'),
                    'allergens': request.form.getlist('allergen'),
                    'instructions': request.form.getlist('instruction'),
                    'spicyness': request.form.get('spicyness', type=int),
                    'difficulty': request.form.get('difficulty', type=int),
                    "type": request.form.get('type')}})
            the_recipe = recipe_coll.find_one({"_id": ObjectId(recipe_id)})

        if g.admin:

            return redirect(url_for('recipe_authorisation'))

        the_user = users_coll.find_one({'email': g.user})
        return render_template('recipe.html', recipe=the_recipe, user=the_user)


@app.route('/admin')
@is_admin
def admin():

    """Entry point for admin functions."""
    return render_template("admin.html")


@app.route('/recipeauthorisation', methods=['GET', 'POST'])
@is_admin
def recipe_authorisation():

    """Display, edit, and authorise, the unauthorised recipes."""
    count = recipe_coll.count_documents({"authorisation": "not"})
    if count > 0:
        unauthorised = recipe_coll.find({"authorisation": "not"})
        authorised = recipe_coll.find({"authorisation": "allowed"})
        users = users_coll.find()

        return render_template("recipeauthorisation.html",
                               unauthorised=unauthorised,
                               authorised=authorised,
                               users=users)

    else:

        return render_template("recipeauthorisation.html")


@app.route('/userauthorisation')
@is_admin
def user_authorisation():

    """Displays user details. """
    users = users_coll.find()

    return render_template("userauthorisation.html", users=users)


@app.route('/deleteuser/<user_id>')
@is_admin
def delete_user(user_id):

    """Deletes a user from the users collection."""
    users_coll.remove({"_id": ObjectId(user_id)})
    users = users_coll.find()

    return render_template("userauthorisation.html", users=users)


@app.route('/makeadmin/<user_id>')
@is_admin
def make_admin(user_id):

    """Sets a user as an admin in the users collection."""
    users_coll.update(
        {'_id': ObjectId(user_id)},
        {'$set': {"admin": True}})
    users = users_coll.find()

    return render_template("userauthorisation.html", users=users)


@app.route('/makeuser/<user_id>')
@is_admin
def make_user(user_id):

    """Sets a user as an admin in the users collection."""
    users_coll.update(
        {'_id': ObjectId(user_id)},
        {'$set': {"admin": False}})
    users = users_coll.find()

    return render_template("userauthorisation.html", users=users)


@app.route('/recipeadmin')
@is_admin
def recipe_overview():

    """Overview of recipes."""
    authorised = recipe_coll.find({"authorisation": "allowed"})

    return render_template("recipeadmin.html", authorised=authorised)


@app.route('/recipeadmin/<recipe_id>')
@is_admin
def delete_recipe(recipe_id):

    """Admin funcction to remove recipe from the database."""
    recipe_coll.remove({"_id": ObjectId(recipe_id)})


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
