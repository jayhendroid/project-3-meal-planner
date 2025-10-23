# TODO: Make requests to the Spoonacular API

import requests
import os

API_KEY = os.getenv("SPOONACULAR_API_KEY")
URL = "https://api.spoonacular.com/recipes/complexSearch"

def gemini_query

def get_diet_recipe_by_meal(meal):
    params = {
    'apiKey': API_KEY,
    'query': meal,
    'number': 5  # Request 5 recipes
    }
    response = requests.get(URL, params=params)
