import os
import pprint
import datetime
import pymongo
from flask import Flask, render_template, redirect, request, url_for, flash, session, g
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from bson.son import SON
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.config["MONGO_DBNAME"] = 'project'
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

mongo = PyMongo(app)

allergens = ['gluten', 'dairy', 'eggs', 'sea food', 'nuts', 'alliums']
types = ['breakfast', 'snack', 'main meal', 'dessert', 'baking']
categories =['vegetarian', 'vegan']

def hrs_to_mins (time_hrs):
    
    """converts time in hours into time in minutes."""
    
    if time_hrs:
        time_mins = int(time_hrs) * 60
    else:
        time_mins = 0
    return time_mins

@app.route('/')
def index():
    
    """Home page with menu."""
    
    votes = mongo.db.recipe.find().sort("votes", pymongo.DESCENDING).limit(4)
    
    return render_template("index.html", votes=votes)
    

@app.before_request
def before_request():
    
    """Sets global user for access control."""
    
    g.user = None
    g.admin = None
    if 'user' in session:
        g.user = session['user']
    if 'type' in session:
        if session['type'] == "admin":
            g.admin = "admin"
    
@app.route('/register', methods=['GET', 'POST'])
def register():
    
    """User registration function."""
    
    if request.method == 'POST':
        email = mongo.db.users.find_one({"email" :request.form.get('email')})
        if email:
            flash("An account for {} already exists, please log in".format(request.form["email"]))
            return redirect(url_for('index'))
        
        if request.form.get('psswd1') == request.form.get('psswd2'):
            password = generate_password_hash(request.form.get('psswd1'))
        registration = {'email': request.form.get('email'), 'username': request.form.get('username'), 'password': password, 'admin': False}
        mongo.db.users.insert_one(registration)
        session['user'] = request.form.get('username')
        
        return redirect(url_for("index"))
    
    return render_template("register.html")
    
    
@app.route('/login', methods=['GET', 'POST'])
def login():

    """Log in function, adds the user to the session allowing access to the full function set."""

    
    if request.form.get('email') and request.form.get('password'):
        login = mongo.db.users.find_one({'email':request.form.get('email')})
        if check_password_hash(login['password'], request.form.get('password')):
            session['user'] = login['username']
            session['email'] = login['email']
            if login['admin']:
                session['type'] = "admin"
                recipes=mongo.db.recipe.find({"authorisation": "not"})
    
                return redirect (url_for("admin", recipes=recipes))
    
    return_url = request.referrer or '/'
    
    return redirect(return_url)
    
    
@app.route('/logout', methods=['POST'])
def logout():
    
    """Log out function, clears the user from the session"""
    
    session.pop('user', None)
    session.pop('type', None)
    g.user = None
    g.admin = None
    
    return_url = request.referrer or '/'
    
    return redirect(return_url)
    

@app.route('/search', methods=['GET', 'POST'])
def search():
    
    """Search function, searches on one or more criterea and passes a subset of recipes to searchresults."""
    
    ingredients = mongo.db.recipe.distinct( "main_ingredients")
    
    return render_template("search.html", ingredients=ingredients, allergens=allergens, types=types, categories=categories)
    
    
@app.route('/searchresults', methods=['GET', 'POST'])
def search_results():
    
    """Takes the results from the search form and displays the matching recipes."""
        
    ingredient_list = []
    allergen_list = []
    type_list = []
    form_data = request.form
    ingredient = False
    recipe_type = False
    recipe_category = []
    category = request.form.get("category")
    
    for key in form_data:
        if 'ingredient' in key:
            ingredient_list.append(form_data[key])
            ingredient = True
        elif 'allergen' in key:
            allergen_list.append(form_data[key])
            allergen = True
        elif 'type'in key:
            type_list.append(form_data[key])
            recipe_type = True
        
    
    spicyness = request.form.get('spicyness', type=int)
    if spicyness is None:
        spicyness = {'$lte': 3}
    difficulty = request.form.get('difficulty', type=int)
    if difficulty is None:
        difficulty = {'$lte': 3}
    time = request.form.get('time', type=int)
    
    if ingredient is True and recipe_type is True:
        recipes = mongo.db.recipe.find({ "main_ingredients": { '$in': ingredient_list }, "allergens": {'$nin': allergen_list}, "type": {'$in': type_list}, "spicyness": spicyness, "difficulty":difficulty, "total_time": {'$lte': time}  } )
    elif ingredient is True:
        recipes = mongo.db.recipe.find({ "main_ingredients": { '$in': ingredient_list }, "allergens": {'$nin': allergen_list}, "spicyness": spicyness, "difficulty": difficulty, "total_time": {'$lte': time} } )
    elif recipe_type is True:
        recipes = mongo.db.recipe.find({"type": {'$in': type_list}, "allergens": {'$nin': allergen_list}, "spicyness": spicyness, "difficulty": difficulty, "total_time": {'$lte': time} } )
    else:
        recipes = mongo.db.recipe.find({ "allergens": {'$nin': allergen_list}, "spicyness": spicyness, "difficulty": difficulty, "total_time": {'$lte': time} })
    
    return render_template("searchresults.html", recipes=recipes ) 
    

@app.route('/browse', methods=['GET', 'POST'])
def browse():
    
    """Display the recipes on individual cards."""
    
    if g.user:
        user = mongo.db.users.find_one({'username': g.user})
        
        return render_template("browse.html", user=user, recipes=mongo.db.recipe.find({"authorisation": "allowed"}))
        
    return render_template("browse.html", recipes=mongo.db.recipe.find({"authorisation": "allowed"}))
    
    
@app.route('/recipe/<recipe_id>')
def recipe(recipe_id):
    
    """Display the selected recipe."""
    
    the_recipe =  mongo.db.recipe.find_one({"_id": ObjectId(recipe_id)})
    the_user = mongo.db.users.find_one( { "notes.id": recipe_id, 'username': g.user } )
    
    return render_template('recipe.html', recipe=the_recipe, user=the_user)
    

@app.route('/vote', methods=['POST'])
def vote():

    """Add a like to the recipe, note user id to disallow multiple likes."""
    
    if g.user:
        if request.method == 'POST':
            recipeID = request.form.get('recipeID')
            votes = request.form.get('votes')
            vote_total = int(votes) + 1
            voted_check = mongo.db.users.find_one({'username': g.user, 'voted': ObjectId(recipeID)})
            if voted_check:
                flash("You have already liked this recipe.")
                
                return redirect (url_for('recipe', recipe_id=recipeID))
                
            else:
                mongo.db.recipe.update({"_id": ObjectId(recipeID)}, {'$set': {'votes': vote_total}})
                mongo.db.users.update({'username': g.user}, {'$push': {'voted':ObjectId(recipeID)}})
            
    return redirect (url_for('recipe', recipe_id=recipeID))


@app.route('/add_favourite', methods=['POST'])
def add_favourite():
    
    """Add a recipe as a favourite."""
    
    if g.user:
        if request.method == 'POST':
            recipeID = request.form.get('recipeID')
            mongo.db.users.update({'username': g.user}, {'$push': {'favourites':recipeID}})
    
    return redirect (url_for('recipe', recipe_id=recipeID))
    

@app.route('/favourites')
def display_favourites():
    
    """List preset favourites, with link to the recipe(s)."""
    
    if g.user:
        user = mongo.db.users.find_one({'username': g.user})
        recipes = mongo.db.recipe.find({"authorisation": "allowed"})
        
        return render_template("favourites.html", user=user, recipes=recipes)
        
    flash("You need to be logged in to see your favourites.")
    return_url =  '/'
    
    return redirect(return_url)


@app.route('/addnote/<recipe_id>', methods=['GET', 'POST'])
def add_note(recipe_id):
    
    """Annotates the recipe with user eneterd text."""
    
    if g.user:
        if request.method == 'POST':
            recipeID = request.form.get('recipeID')
            content = request.form.get('note_content')
            
            # mongo.db.users.update({"username": g.user, "notes.id":recipeID}, { '$set': { "notes.content" : content } })
            # db.users.update( { "email: useremail }, { $set: {"notes": { "id": recipeID, "content": content } } } )
            mongo.db.users.update({'username': g.user}, {'$push': {'notes.id':recipeID, 'notes.content': content}})
            the_recipe =  mongo.db.recipe.find_one({"_id": ObjectId(recipe_id)})
            the_user = mongo.db.users.find_one({"notes.id": recipe_id, 'username': g.user})
            return render_template('recipe.html', recipe=the_recipe, user=the_user)
        
        the_recipe =  mongo.db.recipe.find_one({"_id": ObjectId(recipe_id)})
        the_user = mongo.db.users.find_one({"notes.id": recipe_id, 'username': g.user})
        return render_template('addnote.html', recipe=the_recipe, user=the_user)
    
    return redirect (url_for('browse'))
    
    
@app.route('/notes')
def display_notes():
    
    """Displays all the users notes."""
    
    if g.user:
        notes = mongo.db.users.find({"username": g.user}, {'notes.content': 1, 'notes.id': 1})
        
        return render_template("notes.html", notes=notes)
    
    flash("You must be logged in to view your recipe notes")
    return_url = '/'
    
    return redirect(return_url)
    
    
@app.route('/addrecipe', methods=['GET', 'POST'])
def add_recipe():
    
    """Adds a recipe to the database. Member only area, login required"""
    
    if g.user:
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
            
            mongo.db.recipe.insert_one({"recipe": request.form.get('recipe'), "prep_time": prep_time, "cook_time": cook_time, "total_time": total_time,  "category": request.form.get('category'), "url": request.form.get('url'), "type": request.form.get('type'), "allergens": request.form.get('allergen'), "ingredients": ingredient_list,"main_ingredients": request.form.getlist('main_ingredient'), "instructions": instruction_list, "difficulty": request.form.get('difficulty', type=int), "spicyness": request.form.get('spicyness', type=int), "authorisation": "not", "author": request.form.get('author'), "summary": request.form.get('summary'), "votes": "0"})
            user = mongo.db.users.find_one({'username': g.user})
             
            return render_template("browse.html", user=user, recipes=mongo.db.recipe.find({"authorisation": "allowed"}) )
       
        return render_template("addrecipe.html", allergens=allergens, types=types)
        
    flash("Please log in to use this feature")
    return_url = '/'
    
    return redirect(return_url)
    
    
@app.route('/editrecipe/<recipe_id>', methods=['GET', 'POST'])
def edit_recipe(recipe_id):
    
    """Allows editing of recipes that user entered into the database"""
    
    
    recipe = mongo.db.recipe.find_one({"_id": ObjectId(recipe_id)})
    if g.user == recipe['author'] or session['type'] == "admin":    
        return render_template("editrecipe.html", recipe=recipe, allergens=allergens, types=types)
        
    flash("Only the original author or an admin may edit a recipe.")
    return_url = '/'
    
    return redirect(return_url)


@app.route('/updaterecipe/<recipe_id>', methods=['GET', 'POST'])
def update_recipe(recipe_id):
    
    """Allows editing of recipes that user entered into the database"""
    
    if g.user:
        if request.method == 'POST':
            mongo.db.recipe.update( {'_id': ObjectId(recipe_id)}, 
            {'$set': {
                'type':request.form.get('type'),
                'category':request.form.get('category'),
                'recipe': request.form.get('recipe'),
                'ingredients': request.form.getlist('ingredient'),
                'url':request.form.get('url'),
                'main_ingredients': request.form.getlist('main_ingredient'),
                'summary':request.form.get('summary'),
                'allergens':request.form.get('allergen'),
                'instructions': request.form.getlist('instruction'),
                'spicyness':request.form.get('spicyness'),
                'difficulty':request.form.get('difficulty'),
                "authorisation": request.form.get('authorised')
            }}) 
        
        the_recipe =  mongo.db.recipe.find_one({"_id": ObjectId(recipe_id)})
        
        if session['type'] == "admin":

            return redirect(url_for('recipe_authorisation'))

        return render_template('recipe.html', recipe=the_recipe)
 

@app.route('/admin')
def admin():
    
    """Entry point for admin functions."""
    
    if session['type'] == "admin":
        
        return render_template("admin.html")
        
    flash("Admin access only.")
    return_url = '/'
    
    return redirect(return_url)

    
@app.route('/recipeauthorisation', methods=['GET', 'POST'])
def recipe_authorisation():
    
    """Display, edit, and authorise, the unauthorised recipes."""
    
    if session['type'] == "admin":
        unauthorised = mongo.db.recipe.find({"authorisation": "not"})
        authorised = mongo.db.recipe.find({"authorisation": "allowed"})
        users = mongo.db.users.find()
        
        return render_template("recipeauthorisation.html", unauthorised=unauthorised, authorised=authorised, users=users)
    
    flash("Admin access only.")
    return_url = '/'
    
    return redirect(return_url)
    

@app.route('/userauthorisation')
def user_authorisation():
    
    """Displays user details. Allows a user to be set as an admin."""
    
    if session['type'] == "admin":
        users = mongo.db.users.find()
        
        return render_template("userauthorisation.html", users=users)
        
    flash("Admin access only.")
    return_url = '/'
    
    return redirect(return_url)
    
    
@app.route('/recipeadmin')
def recipe_overview():
    
    """Overview of recipes."""
    
    if session['type'] == "admin":
        authorised = mongo.db.recipe.find({"authorisation": "allowed"})
        
        return render_template("recipeadmin.html", authorised=authorised)
    
    flash("Admin access only.")
    return_url = '/'
    
    return redirect(return_url)


@app.route('/recipeadmin/<recipe_id>')
def delete_recipe(recipe_id):    
    
    """Admin funcction to remove recipe from the database"""
    
    if session['type'] == "admin":
        mongo.db.recipe.remove({"_id": ObjectId(recipe_id)})
        return_url = request.referrer or '/admin'
    
        return redirect(return_url)
        
        #return redirect (url_for("recipe_overview"))
    
    flash("Admin access only.")
    return_url = '/'
    
    return redirect(return_url)
    

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)