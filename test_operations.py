from app.input_sets.models import User, Vote, Recipe, RecipeTag, Tag, RecipeIngredient, Ingredient, Chef
from app import db


Recipe.query.delete()
Ingredient.query.delete()
RecipeIngredient.query.delete()
Chef.query.delete()

newChef = Chef(name="bob")
db.session.add(newChef)
db.session.commit()
chefID = newChef.id

newRecipe1 = Recipe(name="testRecipeName1", description="testRecipeDescription1", creator=chefID, num_votes=1, num_ingredients=3)
db.session.add(newRecipe1)
db.session.commit()

id = newRecipe1.id

carrotRecipe1Ingredient = RecipeIngredient(recipe_id=id)
db.session.add(carrotRecipe1Ingredient)
db.session.commit()
carrotRecipe1Ingredient.set_ingredient_id("carrot", db.session)
db.session.commit()

eggRecipe1Ingredient = RecipeIngredient(recipe_id=id)
db.session.add(eggRecipe1Ingredient)
db.session.commit()
eggRecipe1Ingredient.set_ingredient_id("egg", db.session)
db.session.commit()

beefRecipe1Ingredient = RecipeIngredient(recipe_id=id)
db.session.add(beefRecipe1Ingredient)
db.session.commit()
beefRecipe1Ingredient.set_ingredient_id("beef", db.session)
db.session.commit()



newRecipe2 = Recipe(name="testRecipeName2", description="testRecipeDescription2", creator=chefID, num_votes=50, num_ingredients=2)
db.session.add(newRecipe2)
db.session.commit()

id2 = newRecipe2.id

carrotRecipe2Ingredient = RecipeIngredient(recipe_id=id2)
db.session.add(carrotRecipe2Ingredient)
db.session.commit()
carrotRecipe2Ingredient.set_ingredient_id("carrot", db.session)
db.session.commit()

milkRecipe2Ingredient = RecipeIngredient(recipe_id=id2)
db.session.add(milkRecipe2Ingredient)
db.session.commit()
milkRecipe2Ingredient.set_ingredient_id("milk", db.session)
db.session.commit()



newRecipe3 = Recipe(name="testRecipeName3", description="testRecipeDescription3", creator=chefID, num_votes=0, num_ingredients=2)
db.session.add(newRecipe3)
db.session.commit()

id3 = newRecipe3.id

carrotRecipe3Ingredient = RecipeIngredient(recipe_id=id3)
db.session.add(carrotRecipe3Ingredient)
db.session.commit()
carrotRecipe3Ingredient.set_ingredient_id("carrot", db.session)
db.session.commit()

milkRecipe3Ingredient = RecipeIngredient(recipe_id=id3)
db.session.add(milkRecipe3Ingredient)
db.session.commit()
milkRecipe3Ingredient.set_ingredient_id("milk", db.session)
db.session.commit()



newRecipe4 = Recipe(name="Lemon Garlic Pasta", description="Steph recipe", creator=chefID, num_votes=10, num_ingredients=7)
db.session.add(newRecipe4)
db.session.commit()

id4 = newRecipe4.id

spaghetti = RecipeIngredient(recipe_id=id4)
db.session.add(spaghetti)
db.session.commit()
spaghetti.set_ingredient_id("spaghetti", db.session)
db.session.commit()

oliveOil = RecipeIngredient(recipe_id=id4)
db.session.add(oliveOil)
db.session.commit()
oliveOil.set_ingredient_id("olive oil", db.session)
db.session.commit()

butter = RecipeIngredient(recipe_id=id4)
db.session.add(butter)
db.session.commit()
butter.set_ingredient_id("butter", db.session)
db.session.commit()

lemon = RecipeIngredient(recipe_id=id4)
db.session.add(lemon)
db.session.commit()
lemon.set_ingredient_id("lemon", db.session)
db.session.commit()

parsley = RecipeIngredient(recipe_id=id4)
db.session.add(parsley)
db.session.commit()
parsley.set_ingredient_id("parsley", db.session)
db.session.commit()

garlic = RecipeIngredient(recipe_id=id4)
db.session.add(garlic)
db.session.commit()
garlic.set_ingredient_id("garlic", db.session)
db.session.commit()

parmesanCheese = RecipeIngredient(recipe_id=id4)
db.session.add(parmesanCheese)
db.session.commit()
parmesanCheese.set_ingredient_id("parmesan cheese", db.session)
db.session.commit()