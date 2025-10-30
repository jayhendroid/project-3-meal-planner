# pip install -q -U google-generativeai
# The purpose of this file is to use Gemini API to generate meal recipes using Spoonacular API data

import google.generativeai as genai
import os

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
AImodel = genai.GenerativeModel(model_name="gemini-1.5-flash")

# Generate text using Gemini API, prompt is the input string given by the user
def gemini_query(prompt):
    response = AImodel.generate_text(
        prompt=prompt,
        max_output_tokens=500,
        temperature=0.7,
        top_p=0.9,
    )
    return response.text

# Create a recipe_info function that takes in meal, intolerances, diet, and calorieTarget, 
# as well as the recipe information from Spoonacular API including recipe titles and calorie information
# this function will NOT create the prompt, just format the information for the prompt creation
def recipe_info(meal, intolerances, diet, calorieTarget, recipes):
    meal_data = {
        'meal': meal,
        'intolerances': intolerances,
        'diet': diet,
        'calorieTarget': calorieTarget,
        'recipes': recipes
    }
    return meal_data


# TODO add system prompt using the information above
