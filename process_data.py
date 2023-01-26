import pandas as pd
from app.input_sets.models import User, Vote, Recipe, RecipeTag, Tag, RecipeIngredient, Ingredient, Chef
from app import db

Recipe.query.delete()
Ingredient.query.delete()
RecipeIngredient.query.delete()
Chef.query.delete()

df = pd.read_csv('RAW_recipes.csv')

df.drop(['id','submitted','tags','nutrition'], axis=1,inplace = True)
df['ingredients'] = df.ingredients.apply(lambda x: x.replace('[','')) 
df['ingredients'] = df.ingredients.apply(lambda x: x.replace(']','')) 
df['ingredients'] = df.ingredients.apply(lambda x: x[1:-1].split(','))
df.fillna('', inplace=True)

for index, row in df.head(10000).iterrows():

    if index % 100 == 0:
        print("Batch " + str(index) + " complete.")

    #make chef
    chef = Chef.query.filter_by(name=str(row.contributor_id)).first()
    if chef == None:
        chef = Chef(name=str(row.contributor_id))
        db.session.add(chef)
        db.session.commit()
    chefID = chef.id
    
    newRecipe = Recipe(name=row['name'], description=row.description, creator=chefID, num_votes=0, num_ingredients=row.n_ingredients)
    db.session.add(newRecipe)
    db.session.commit()

    recipeID = newRecipe.id

    for j in row.ingredients:
        j = j.replace("'", "")
        j = j.lstrip() #remove leading spaces

        
        newRecipeIngredient = RecipeIngredient(recipe_id=recipeID)
        db.session.add(newRecipeIngredient)
        db.session.commit()
        newRecipeIngredient.set_ingredient_id(j, db.session)
        db.session.commit()

print("DONE!")