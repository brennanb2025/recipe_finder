from flask import request, render_template, flash, redirect, url_for, session, make_response, send_from_directory
from app import app, db#, s3_client, oauth
#import lm as well?^
from app.input_sets.forms import LoginForm, RegistrationForm
from app.input_sets.models import User, Vote, Recipe, RecipeTag, Tag, RecipeIngredient, Ingredient
from werkzeug.utils import secure_filename
from werkzeug.exceptions import HTTPException
import datetime
import re
from flask_wtf.csrf import CSRFError
import datetime
#import boto3
#import imghdr
#from flask_login import (
    #current_user,
    #login_required,
    #login_user,
    #logout_user,
    #LoginManager
#)
#from oauthlib.oauth2 import WebApplicationClient
import requests
from datetime import timedelta
from flask import jsonify
#from requests_oauthlib import OAuth2Session
#import json

from sqlalchemy import select, func, desc, and_
from sqlalchemy.sql import label

#TODO: ADD  and form.validate():   to protect forms


#session timeout
@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(hours=10) #10 hours until need to resign in

#different urls that application implements
#v=decorators, modifies function that follows it. Creates association between URL and fxn.
@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET']) 
def index():
    
    return render_template('index.html', userID=session.get('userID'))

@app.route('/sign-in', methods=['GET'])
def sign_in():

    if userLoggedIn(): #valid session token -- user already logged in
        return redirect(url_for('view', id=session['userID']))

    form = LoginForm()
    title="Sign in"
    return render_template('sign_in.html', form=form, title=title)

@app.route('/sign-in', methods=['POST'])
def sign_inPost():

    form1 = request.form 
    
    success = True
    if form1.get('email') == "": #no email entered
        success = False
        flash(u'Please enter an email', 'emailError')
    if form1.get('password') == "": #no password entered
        flash(u'Please enter a password', 'passwordError')
        success = False
    if success: #they entered an email and password - now check them
        if User.query.filter_by(email=form1.get('email')).first() == None: #email entered but not found
            success = False
            flash(u'User does not exist. If you are a new user, click the "Make an Account" button below.', 'emailError')
        elif not User.query.filter_by(email=form1.get('email')).first().check_password(form1.get('password')): #email and password do not match
            flash(u'Incorrect password', 'passwordError')
            success = False
    if success: 
        user = User.query.filter_by(email=form1.get('email')).first()
        id = user.id
        resp = make_response(redirect(url_for('view', id=id))) #get view should send to main page
        resp.set_cookie('userID', str(id))

        session["userID"] = id
        #newToken = SessionTokens(sessionID=sessionToken) #make a new token
        #db.session.add(newToken) #add to database
        
        return resp
    else:
        return redirect(url_for('sign_in')) #failure


@app.route('/register', methods=['GET'])
def register():

    # Attempts to register an email/password pair 
    form = RegistrationForm()

    if userLoggedIn():
        return redirect(url_for('view', id=session.get('userID')))
    
    return render_template('register.html', form=form)


#Current file size limited to 5 MB - with free tier AWS (5GB S3) this limits to a minimum of 1024 images.
@app.route('/register', methods=['POST'])
def registerPost():

    form1 = request.form   
    
    (success, errors) = checkBasicInfo(form1)

    if success: #success, registering new user
        
        
        user = User(email=form1.get('email'), first_name=form1.get('first_name'), last_name=form1.get('last_name'))
        
        db.session.add(user) #add to database
        user.set_password(form1.get('password')) #must set pwd w/ hashing method
        db.session.commit()
        

        return redirect(url_for('sign_in')) #success: get request to sign_in page
    else:
        return registerPreviouslyFilledOut(form1, errors)


def registerPreviouslyFilledOut(form, errors):

    email = form.get("email")
    first_name = form.get("first_name")
    last_name = form.get("last_name")
    

    if "email" in errors: #if error - make it blank.
        email = ""
    if "first name" in errors:
        first_name = ""
    if "last name" in errors:
        last_name = ""


    #v load the register page
    formNew = RegistrationForm()

    if userLoggedIn():
        return redirect(url_for('view', id=session.get('userID')))

    return render_template('register.html', email=email, first_name=first_name, last_name=last_name, form=formNew)
    

def checkBasicInfo(form1):
    errors = []
    success = True
    if User.query.filter_by(email=form1.get('email')).first() != None: #email taken
        success = False
        flash(u'Email taken. Please enter a different email.', 'emailError')
        errors.append("email")
    if form1.get('email') == '':
        success = False
        flash(u'Please enter an email.', 'emailError')
        errors.append("email")
    else:
        regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$' #if it isn't a valid email address
        if(not(re.search(regex,form1.get('email')))):
            flash('Invalid email address', 'emailError')
            success = False
            errors.append("email")
    if form1.get('first_name') == '':
        success = False
        flash(u'Please enter a first name.', 'first_nameError')
        errors.append("first name")
    if form1.get('last_name') == '':
        success = False
        flash(u'Please enter a last name.', 'last_nameError')
        errors.append("last name")
    if form1.get('password') == '':
        success = False
        flash(u'Please enter a password.', 'passwordError')
        #errors.append("password") not used for anything - passwords are wiped anyway
    if form1.get('password2') == '':
        success = False
        flash(u'Please reenter your password.', 'password2Error')
        #errors.append("password") not used for anything - passwords are wiped anyway
    if success: #did enter everything
        if form1.get('password') != form1.get('password2'): #passwords don't match
            success = False
            flash(u'Passwords do not match.', 'password2Error')
            #errors.append("password") not used for anything - passwords are wiped anyway
    
    return (success, errors)



@app.route('/view', methods=['GET']) #takes one arg = user.id. This is the user that the person logged in is viewing. Doesn't have to be the same user.
def view():
    #sessionID1 = request.cookies.get("user") #get the session token from the previous page cookies

    if not(userLoggedIn()):
        flash(u'You must log in.', 'loginRedirectError')
        return redirect(url_for('sign_in'))

    if request.args.get("id") == None: #they went to view get without a user id in the request args
        return redirect(url_for('index'))

    user = User.query.filter_by(id=request.args.get("id")).first() #get the correct profile by inputting user id
    if user == None:
        return not_found("404")

    first = user.first_name
    last = user.last_name

    votes = user.rtn_votes()
    recipesLiked = []
    for v in votes:
        recipesLiked.append(Recipe.query.filter_by(id=v.recipe_id).first())

    this_user_is_logged_in = (user.id == session.get('userID'))

    #^if the user looking at this person's profile page is the one who is currently logged in, 
    # let them logout from or delete their account.
    return render_template('view.html', logged_in=this_user_is_logged_in, first=first, last=last, 
            recipesLiked=recipesLiked, userID=session.get("userID"))
    #user logged in: show profile page.

@app.route('/logout', methods=['GET'])
def logout():
    #means they hit logout btn
    if session.get('userID'): #valid session token -- user already logged in
        session.pop('userID', None)

    return redirect(url_for('index'))
    
@app.route('/deleteProfile', methods=['POST'])
def deleteProfile():
    form1 = request.form
    
    #valid session token -- user already logged in  
    if not(userLoggedIn()):
        return redirect(url_for('sign_in'))
    
    userID = session.get('userID')
    session.pop('userID', None)

    #DELETE VOTES
    Vote.query.filter_by(user_id=userID).delete()

    User.query.filter_by(id=userID).delete()

    db.session.commit()

    return redirect(url_for('sign_in'))


def get_popular_ingredients(): 
    ingredients = Ingredient.query.order_by(Ingredient.num_use.desc()).limit(500).all() #sort by num_use and limit to 200
    return ingredients

@app.route('/find-recipe', methods=['GET'])
def find_recipe():

    get = True

    logged_in = userLoggedIn()

    ingredients = get_popular_ingredients()
    
    return render_template('find_recipe.html', get=get, ingredients=ingredients, logged_in=logged_in, userID=session.get("userID"))

@app.route('/find-recipe/<int:page>', methods=['POST'])
def find_recipe_post(page):
    form = request.form

    ingredients = form.getlist("ingredientName")
    
    #search for recipes using these ingredients.
    """
    I changed this so it no longer uses recipeIngredients and just uses ingredients!!!!!
    """
    ingredientsIdList = []
    recipeIngredientsList = [] #list of RecipeIngredient objects
    for r in ingredients:
        ingredientObject = Ingredient.query.filter_by(name=r).first()
        if ingredientObject != None:
            ingredientsIdList.append(ingredientObject.id)
            recipeIngredients = RecipeIngredient.query.filter_by(ingredient_id=ingredientObject.id).all()
            for ri in recipeIngredients:
                recipeIngredientsList.append(ri.id)
    #I have recipe names --> I get all RecipeIngredients that utilize those recipes.
    #Because RecipeIngredients are what links Recipes with Ingredients.


    #ADD OPTIONS:
    # % ingredients match descending
    # number ingredients match ascending
    # number ingredients needed ascending

    per_page = 10
    recipes = db.session.query( \
            label("recipe_id", Recipe.id),
            #Ingredient,
            label("number_ingredient_matches", func.count(Recipe.id) ),
            label("percent_ingredients_fulfilled", (func.count(Recipe.id) + 0.0) / Recipe.num_ingredients),
            label("num_ingredients_needed", Recipe.num_ingredients - func.count(Recipe.id)),
            label("RecipeIngredient_id", RecipeIngredient.id),
            label("Recipe_id", Recipe.id)
        ).outerjoin(RecipeIngredient, Recipe.id == RecipeIngredient.recipe_id) \
        .outerjoin(Ingredient, RecipeIngredient.ingredient_id == Ingredient.id) \
        .filter(
            Ingredient.id.in_(ingredientsIdList)
            #RecipeIngredient.id.in_(recipeIngredientsList)
        ).group_by(
            Recipe.id
        ).order_by(
            #"number_ingredient_matches",
            desc("percent_ingredients_fulfilled"),
            "num_ingredients_needed",
            desc(Recipe.num_votes)
        ).paginate(page,per_page,error_out=False)
    
    """
    This was right after the outerjoin and before the group by
    .filter(
            RecipeIngredient.id.in_(recipeIngredientsList)
        )
    """


    """
    SELECT 
        Recipe,
        Ingredient,
        COUNT(Recipe.id) AS number_ingredient_matches
        (COUNT(Recipe.id) + 0.0) / Recipe.num_ingredients AS percent_ingredients_fulfilled
    FROM
        LEFT JOIN
            RecipeIngredient, Recipe
        ON Recipe.id = RecipeIngredient.recipe_id
        LEFT JOIN
            Ingredient, RecipeIngredient
        ON RecipeIngredient.ingredient_id = Ingredient.id
        WHERE
            RecipeIngredient.id IN recipeIngredientsList
    GROUP BY
        Recipe.id
    ORDER BY
        percent_ingredients_fulfilled descending
        Recipe.num_votes descending
    """


    recipeItems = recipes.items
    recipeItemsLen = recipes.total
    

    if recipeItemsLen == 0:
        ingredients = []
    else:
            
        #The problem is that query uniquifies my results. 
        #So in the actual join, I have multiple rows with the same recipe.id
        #And the count reflects that. But then when I return it, sqlalchemy applies 
        #Further logic onto the query results.
        #Solution (maybe temporary): I have to do more work.
        #I have the recipes. I left outer join recipeIngredients onto Ingredients.
        #I filter the recipeIngredients by the ones in the recipe list
        #and then group by recipeIngredient ids.

        #Links:
        # https://github.com/sqlalchemy/sqlalchemy/issues/4395
        # https://stackoverflow.com/questions/6933478/sqlalchemy-only-one-result-being-returned-when-count-says-there-are-more

        ingredients = db.session.query( \
                #RecipeIngredient, 
                Ingredient,
                label("recipe_id", RecipeIngredient.recipe_id)
        ).outerjoin(Ingredient, RecipeIngredient.ingredient_id == Ingredient.id) \
        .filter(
            Ingredient.id.in_(ingredientsIdList)
            #RecipeIngredient.id.in_(recipeIngredientsList)
        ).all()
        """
        SELECT
            Ingredient,
            RecipeIngredient.recipe_id as recipe_id
        FROM
            LEFT JOIN
                Ingredient,
                RecipeIngredient
            ON
                RecipeIngredient.ingredient_id = Ingredient.id
            WHERE
                RecipeIngredient.id IN recipeIngredientsList

        """

        #Note: I select Recipe.id from ingredients, recipes --> 
        # so ingredient.id will correspond to it's corresponding recipe's id.


    #Now get ALL of the ingredients for each recipe
    recipeIDList = []
    for r in recipeItems:
        recipeIDList.append(r.recipe_id)
    
    if recipeItemsLen == 0:
        allIngredients = []
    else:
        allIngredients = get_ingredients(recipeIDList)

    if recipeItemsLen == 0:
        recipeList = []
    else:
        allIngredientTable = {}
        for i in allIngredients:
            if allIngredientTable.get(i.recipe_id) != None: #already has this recipe
                ingredientsArr = allIngredientTable[i.recipe_id]
                ingredientsArr.append(i.Ingredient)
                allIngredientTable[i.recipe_id] = ingredientsArr #add to ingredients array
            else:
                ingredientsArr = [] #put empty ingredients array
                ingredientsArr.append(i.Ingredient)
                allIngredientTable[i.recipe_id] = ingredientsArr

        ingredientTable = {} #recipe.id : [ingredients fulfilled]
        for i in ingredients:
            if ingredientTable.get(i.recipe_id) != None: #already has this recipe
                ingredientsArr = ingredientTable[i.recipe_id]
                ingredientsArr.append(i.Ingredient)
                ingredientTable[i.recipe_id] = ingredientsArr #add to ingredients array
            else:
                ingredientsArr = [] #put empty ingredients array
                ingredientsArr.append(i.Ingredient)
                ingredientTable[i.recipe_id] = ingredientsArr

        uniqueRecipes = {} #dict of recipe : ([ingredients fulfilled], #ingredients fulfilled)
        for r in recipeItems:
            if uniqueRecipes.get(r.recipe_id) == None:
                uniqueRecipes[r.recipe_id] = (ingredientTable[r.recipe_id], allIngredientTable[r.recipe_id], r.number_ingredient_matches)

        recipeList = []
        for r in uniqueRecipes.keys():
            recipeList.append((Recipe.query.filter_by(id=r).first(), uniqueRecipes[r][0], uniqueRecipes[r][1], uniqueRecipes[r][2]))

    get = False

    logged_in = userLoggedIn()

    ingredients = get_popular_ingredients()

    return render_template('find_recipe.html', get=get, logged_in=logged_in, ingredients=ingredients,
            recipeList=recipeList, recipes=recipes,
            userID=session.get("userID"))


def get_ingredients(recipeIDList):
    return db.session.query( \
            Ingredient,
            label("recipe_id", RecipeIngredient.recipe_id)
    ).outerjoin(Ingredient, Ingredient.id == RecipeIngredient.ingredient_id) \
    .filter(
        RecipeIngredient.recipe_id.in_(recipeIDList)
    ).all()
    """
    SELECT
        Ingredient,
        RecipeIngredient.recipe_id AS recipe_id
    FROM
        LEFT JOIN
            Ingredient, RecipeIngredient
        ON
            Ingredient.id == RecipeIngredient.ingredient_id
        WHERE
            RecipeIngredient.recipe_id.in_(recipeIDList)
    
    """


@app.route('/view-recipe', methods=['GET'])
def view_recipe():
    if request.args.get("id") == None: #they went to view-recipe get without a recipe id in the request args
        return redirect(url_for('index'))

    recipe = Recipe.query.filter_by(id=request.args.get("id")).first() #get the correct profile by inputting user id
    if recipe == None:
        return not_found("404")

    recipeIDList = []
    recipeIDList.append(recipe.id)
    ingredients = get_ingredients(recipeIDList)
    ingredients = [i.Ingredient.name for i in ingredients]
    

    #^if the user looking at this person's profile page is the one who is currently logged in, 
    # let them logout from or delete their account.
    return render_template('view_recipe.html', name=recipe.name, description=recipe.description,
        num_votes=recipe.num_votes, creator=recipe.creator, num_ingredients=recipe.num_ingredients,
        ingredients=ingredients,
        userID=session.get("userID"))
    #user logged in: show profile page.






def userLoggedIn():
    #Checks if the user is actually logged in -- commented out for easier testing
    #userID = SessionTokens.query.filter_by(sessionID=sessionID1).first()
    if session.get('userID'): #valid session token -- user already logged in
        if User.query.filter_by(id=session['userID']).first() == None:
            return False
        return True

    return False


"""
Commented out for testing
@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    return render_template('csrf_error.html', reason=e.description), 400

@app.errorhandler(404)
# inbuilt function which takes error as parameter
def not_found(e):
    # defining function
    return render_template("404_error.html")

@app.errorhandler(Exception)
# inbuilt function which takes error as parameter
def error_handler(e):
    code = 500 #problem with my code
    if isinstance(e, HTTPException):
        code = e.code
    if code == 404:
        return render_template("404_error.html")
    if code == 500:
        db.session.rollback()
    
    return render_template("general_error.html", code=code)

"""