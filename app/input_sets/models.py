from jmespath import search
from app import db, Base
#from sqlalchemy import DateTime, Float, Boolean, ForeignKey
#from sqlalchemy.orm import relationship
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(UserMixin, db.Model, Base): #inherits from db.Model, base for flask-SQLAlchemy
    #class User(UserMixin):

    __tablename__ = "User"
    
    id = db.Column(db.Integer, primary_key=True) #id = primary key
    email = db.Column(db.String(64), index=True, unique=True) #defined as strings, max length = ().
    password_hash = db.Column(db.String(128)) #not storing plaintext pwd, hashing first.
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
 
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    votes = db.relationship(
        'Vote',
        backref='User', 
        lazy='dynamic',
        primaryjoin="Vote.user_id == User.id" 
    )


    def rtn_votes(self):
        arr = []
        for vote in self.votes:
            arr.append(vote)
        return arr


    #in case user wants to change profile
    def set_first_name(self, first_name): 
        self.first_name = first_name

    def set_last_name(self, last_name):
        self.last_name = last_name

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def set_isStudent(self, isStudent):
        self.is_student=isStudent

    def check_password(self, password):
        return check_password_hash(self.password_hash, password) #<^=pwd hashing logic
    
    def __repr__(self):
        return '<User {}>'.format(self.email + " " + self.first_name + " " + self.last_name) #how to print database


class Chef(db.Model, Base):
    __tablename__ = "Chef"

    id = db.Column(db.Integer, primary_key=True) #id = primary key
    name = db.Column(db.String(128))

    recipes = db.relationship(
        'Recipe',
        backref='Chef', 
        lazy='dynamic',
        primaryjoin="Recipe.creator == Chef.id" 
    )

    def rtn_recipes(self):
        arr = []
        for r in self.recipes:
            arr.append(r)
        return arr


class Recipe(db.Model, Base):
    __tablename__ = "Recipe"
    
    id = db.Column(db.Integer, primary_key=True) #id = primary key

    name = db.Column(db.String(128))
    description = db.Column(db.String(8192)) #about 2000 characters
    num_votes = db.Column(db.Integer)
    creator = db.Column(db.Integer, db.ForeignKey(Chef.id))

    num_ingredients = db.Column(db.Integer)


    def inc_num_votes(self):
        self.num_votes = self.num_votes+1
    
    def dec_num_votes(self):
        self.num_votes = self.num_votes-1

    def __repr__(self):
        return '<Recipe {}>'.format(self.name + " " + str(self.creator) + " " + self.description + " " + str(self.num_ingredients) + " " + str(self.num_votes)) #how to print database



class Ingredient(db.Model, Base):

    __tablename__ = "Ingredient"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    num_use = db.Column(db.Integer)

    def inc_num_use(self):
        self.num_use = self.num_use+1
    
    def dec_num_use(self):
        self.num_use = self.num_use-1

    def __repr__(self):
        return '<Ingredient {}>'.format(str(self.id) + " " + self.name + " " + str(self.num_use)) #how to print database


class RecipeIngredient(db.Model, Base):
    __tablename__ = "RecipeIngredient"
    
    id = db.Column(db.Integer, primary_key=True) #id = primary key

    recipe_id = db.Column(db.Integer, db.ForeignKey(Recipe.id))
    ingredient_id = db.Column(db.Integer, db.ForeignKey(Ingredient.id))

    def delete_inc(self):
        searchIngredient = Ingredient.query.filter_by(id=self.ingredient_id).first() #will exist
        searchIngredient.dec_num_use()
        db.session.commit()

    def set_ingredient_id(self, ingredientName, session): #must check for duplicates, else add new ingredient
        searchIngredient = Ingredient.query.filter_by(name=ingredientName.lower()).first()
        if searchIngredient == None: #this tag does not yet exist
            newIngredient = Ingredient(name=ingredientName.lower(), num_use=0) #set actual ingredient saved to lowercase
            session.add(newIngredient)
            session.commit() #have to do this before for the id to set
            self.ingredient_id = newIngredient.id
            newIngredient.inc_num_use()
            session.commit()
        else:
            self.ingredient_id = searchIngredient.id
            searchIngredient.inc_num_use()
            session.commit()



class Tag(db.Model, Base):

    __tablename__ = "Tag"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))

    num_use = db.Column(db.Integer)

    def inc_num_use(self):
        self.num_use = self.num_use+1
    
    def dec_num_use(self):
        self.num_use = self.num_use-1

class RecipeTag(db.Model, Base):
    __tablename__ = "RecipeTag"
    
    id = db.Column(db.Integer, primary_key=True) #id = primary key

    recipe_id = db.Column(db.Integer, db.ForeignKey(Recipe.id))
    tag_id = db.Column(db.Integer, db.ForeignKey(Tag.id))

    def set_tag_id(self, tagName, session): #must check for duplicates, else add new tag
        searchTag = Tag.query.filter_by(title=tagName.lower()).first()
        if searchTag == None: #this tag does not yet exist
            t1 = Tag(title=tagName.lower(), num_use=0) #set actual tag saved to lowercase
            session.add(t1)
            session.commit() #have to do this before for the id to set
            self.tag_id = t1.id
            session.commit()
        else:
            self.tag_id = searchTag.id
            session.commit()




class Vote(db.Model, Base):
    __tablename__ = "Vote"

    id = db.Column(db.Integer, primary_key=True) #id = primary key

    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    recipe_id = db.Column(db.Integer)
