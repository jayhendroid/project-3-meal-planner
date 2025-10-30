# pip install -q -U google-generativeai
# The purpose of this file is to use Gemini API to generate meal recipes using Spoonacular API data

import google.generativeai as genai
import os

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
AImodel = genai.GenerativeModel(model_name="gemini-1.5-flash")

# Generate text using Gemini API based on the provided prompt below
def gemini_query(prompt):
    response = AImodel.generate_text(
        prompt=prompt,
        max_output_tokens=500,
        temperature=0.7,
        top_p=0.9,
    )
    return response.text

# Create recipe_info function to structure recipe information
def recipe_info(meal, intolerances, diet, calorieTarget, recipe_info_list):
    meal_data = {
        'meal': meal,
        'intolerances': intolerances,
        'diet': diet,
        'calorieTarget': calorieTarget,
        'recipes': recipe_info_list
    }
    return meal_data

# Create user_prompt function to format the user input and recipe information into a prompt for Gemini API
def user_prompt(user_input):
    Meal_Data = f"""Meal: {user_input['meal']}
Intolerances: {user_input['intolerances']}
Diet: {user_input['diet']}
Calorie Target: {user_input['calorieTarget']}
Recipes: {user_input['recipes']}
"""
    return Meal_Data


# Create system_prompt function to provide instructions to Gemini API for generating meal recipes
def system_prompt():
    prompt = f"""Using the meal data provided by the user, generate a detailed meal recipe 
    with step by step instructions, catering to the user's dietary preferences, inolerances, and calorie target.
    Use the recipes provided by the user data as inspiration."""
    return prompt

