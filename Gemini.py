# pip install -q -U google-generativeai
# The purpose of this file is to use Gemini API to generate meal recipes using Spoonacular API data

import google.generativeai as genai
import os

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

# Generate text using Gemini API, prompt is the input string given by the user
def gemini_query(prompt):
    response = model.generate_text(
        prompt=prompt,
        max_output_tokens=500,
        temperature=0.7,
        top_p=0.9,
    )
    return response.text

def user_prompt(meal, recipes):
    prompt = f"Generate a detailed recipe for {meal} using the following recipes as references:\n\n"
    for i, recipe in enumerate(recipes, 1):
        prompt += f"Recipe {i}:\nTitle: {recipe['title']}\nLink: {recipe['sourceUrl']}\nSummary: {recipe['summary']}\n\n"
    prompt += "Please provide a step-by-step recipe including ingredients and instructions."
    return prompt