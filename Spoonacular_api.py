import requests
import logging
import os
from dotenv import load_dotenv

# Load environment variables from KEYS.env
load_dotenv("KEYS.env")

API_KEY = os.getenv("SPOONACULAR_API_KEY")
URL = "https://api.spoonacular.com/recipes/complexSearch"

if not API_KEY:
    raise ValueError("Missing SPOONACULAR_API_KEY in KEYS.env")

# Get diet recipes by diet name from Spoonacular API
def get_diet_recipes_by_diet(diet=None, intolerances=None, calorieTarget=None):
    params = {
        'apiKey': API_KEY,
        'number': 5  # Request 5 recipes
    }

    # Only add optional parameters if they are provided
    if diet:
        params['diet'] = diet
    if intolerances:
        params['intolerances'] = intolerances
    if calorieTarget:
        params['maxCalories'] = calorieTarget

    try:
        response = requests.get(URL, params=params, timeout=10)
        print("Spoonacular request URL:", response.url)
        print("Status code:", response.status_code)

        if response.status_code == 401:
            return None, "Invalid Spoonacular API key or quota exceeded."
        elif response.status_code == 404:
            return None, "No recipes found for the given criteria."

        response.raise_for_status()  # Raise error for 4xx or 5xx responses
        recipes = response.json()
        return recipes, None

    except requests.exceptions.RequestException as e:
        logging.exception(e)
        print("Spoonacular request failed:", e)
        return None, f"Error connecting to Spoonacular API: {e}"


# Function to extract relevant recipe information
def get_recipe_information(json_response):
    recipe_info_list = []
    for recipe in json_response.get('results', []):
        recipe_info = {
            'title': recipe.get('title'),
            'id': recipe.get('id'),
            'image': recipe.get('image', 'N/A'),
            'calories': recipe.get('calories', 'N/A')
        }
        recipe_info_list.append(recipe_info)
    return recipe_info_list
