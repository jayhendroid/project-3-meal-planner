from flask import Flask, render_template, request
from Spoonacular_api import get_diet_recipes_by_diet
from Gemini import user_prompt

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
    recipes, error = get_diet_recipes_by_diet('dinner', restrictions, target_calories, diet)
    if error:
        return render_template('error.html', error=error)

    # Pass everything to the template
    return render_template(
        'plan.html',
        diet=diet,
        restrictions=restrictions,
        target_calories=target_calories,
        plan=plan,
        plan_md=None  # fallback not needed for now
    )

if __name__ == '__main__':
    app.run(debug=True)