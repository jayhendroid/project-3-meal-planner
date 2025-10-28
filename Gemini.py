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

# Create a prompt for Gemini using the params and Spoonacular recipes
# def user_prompt(meal, recipes, intolerances, diet, calorieTarget):
    # prompt = f"Create a detailed meal recipe for {meal} considering the following recipes from Spoonacular API:\n"
    # for recipe in recipes:
    #     prompt += f"- {recipe['title']} 
    # prompt += f"""\nThe meal should never exceed or significantly fall short of the calorie target {calorieTarget}, 
    # must consider the following intolerances: {intolerances}, 
    # and should follow the user's dietary strategy {diet}.\n"""
    # prompt += "Provide a step-by-step recipe with ingredients and instructions."
    # return prompt

# TODO add system prompt using the information above
