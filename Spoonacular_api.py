# TODO: Make requests to the Spoonacular API 

import requests
import os

API_KEY = os.getenv("SPOONACULAR_API_KEY")
URL = "https://api.spoonacular.com/recipes/complexSearch"

# Get diet recipes by meal name from Spoonacular API
# 'meal', 'maxCalories', etc will come from user input in the Flask app
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
    recipes = response.json()  # parse JSON response into a Python dictionary
    return recipes['results']   # results contains the list of recipes


# Function to extract relevant recipe information from Spoonacular API response
# Returns a dictionary with key information for a single recipe
def get_recipe_information(json_response):
    recipe_info = {
        'title': json_response.get('title'),
        'id': json_response.get('id'),
        'calories': json_response.get('calories', 'N/A')  # N/A if calories info is not available
    }
    return recipe_info
