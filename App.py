from flask import Flask, render_template, request
from Spoonacular_api import get_diet_recipes_by_diet
from Gemini import gemini_query, recipe_info, user_prompt, system_prompt

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html') # Home Page

# Route to handle the form submission and generate dietary recipe based on user input
@app.route('/plan', methods=['POST'])
def plan():
    # Grab user input from the form
    diet = request.form.get('diet')
    restrictions = request.form.get('restrictions')
    target_calories = request.form.get('target_calories')

    # Get recipes from Spoonacular API
    recipes, error = get_diet_recipes_by_diet(diet, restrictions, target_calories)
    if error:
        return render_template('error.html', error=error)
    
    # Give the recipe data to Gemini API to generate dietary recipe
    recipe_info_list = recipe_info(diet, restrictions, target_calories, recipes)
    user_input = user_prompt(recipe_info_list)
    system_instructions = system_prompt()
    query_prompt = f"{system_instructions}\n\n{user_input}"
    dietary_recipe = gemini_query(query_prompt)

    # Pass everything to the template
    return render_template(
        'plan.html',
        diet=diet,
        restrictions=restrictions,
        target_calories=target_calories,
        dietary_recipe=dietary_recipe,
        plan_md=None  # fallback not needed for now
    )

if __name__ == '__main__':
    app.run(debug=True)