import json
from flask import Flask, render_template, request
from Spoonacular_api import get_diet_recipes_by_diet, get_recipe_information
from Gemini import gemini_query, recipe_info, user_prompt, system_prompt

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/plan', methods=['POST'])
def plan():
    diet = request.form.get('diet')
    restrictions = request.form.get('restrictions')
    target_calories = request.form.get('target_calories')

    # Get recipes from Spoonacular API
    recipes, error = get_diet_recipes_by_diet(diet, restrictions, target_calories)
    if error:
        return render_template('error.html', error=error)

    # Extract relevant recipe info
    recipe_info_list = get_recipe_information(recipes)
    user_input = recipe_info(diet, restrictions, target_calories, recipe_info_list)
    query_prompt = f"{system_prompt()}\n\n{user_prompt(user_input)}"

    # Call Gemini API
    gemini_response = gemini_query(query_prompt)

    # Debug: print raw Gemini output in terminal
    print("=== GEMINI RAW OUTPUT ===")
    print(gemini_response)
    print("========================")

    # Try to parse JSON; fallback to plain text if parsing fails
    try:
        dietary_recipe_list = json.loads(gemini_response)
        # Ensure it is a list of recipes
        if not isinstance(dietary_recipe_list, list):
            dietary_recipe_list = [{
                "title": "Recipe generation",
                "ingredients": [],
                "instructions": gemini_response
            }]
    except json.JSONDecodeError:
        # If JSON parsing fails, just show raw text in a single recipe
        dietary_recipe_list = [{
            "title": "Recipe generation",
            "ingredients": [],
            "instructions": gemini_response
        }]

    return render_template(
        'plan.html',
        diet=diet,
        restrictions=restrictions,
        target_calories=target_calories,
        dietary_recipe_list=dietary_recipe_list
    )

if __name__ == '__main__':
    app.run(debug=True)