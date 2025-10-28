# TODO: Make requests to the Spoonacular API 

import requests
import os

API_KEY = os.getenv("SPOONACULAR_API_KEY")
URL = "https://api.spoonacular.com/recipes/complexSearch"

# Get diet recipes by meal name from Spoonacular API
# 'meal' will come from user input in the Flask app
def get_diet_recipes_by_meal(meal, intolerances, calorieTarget, diet):
    params = {
    'apiKey': API_KEY,
    'query': meal,
    'maxCalories': calorieTarget,
    'diet': diet,
    'intolerances': intolerances,
    'number': 5  # Request 5 recipes
    }

    response = requests.get(URL, params=params)
    mealdata = response.json()
    
    # Process the JSON response
    for recipe in mealdata['results']:
        print(f"Title: {recipe['title']}")
        print(f"Recipe ID: {recipe['id']}")
        print(f"Calories: {recipe.get('calories', 'N/A')}")
        print(f"Diet: {diet}")
        print("-" * 20)

    return mealdata['results']


# TODO: the 'params' fields in the above function will be populated by user input from the Flask app
# This can be changed to include diet preferences, as well as other parameters like cuisine, intolerances, etc.