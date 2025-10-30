from flask import Flask, render_template, request
from Spoonacular_api import get_diet_recipes_by_meal
from Gemini import user_prompt

from flask import Flask, render_template, request
from Spoonacular_api import get_diet_recipes_by_meal
from Gemini import user_prompt

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/plan', methods=['POST'])
def plan():
    # Grab user input from the form
    diet = request.form.get('diet')
    restrictions = request.form.get('restrictions')
    target_calories = request.form.get('target_calories')

    # Example: structured fake meal plan (to test plan.html layout)
    plan = [
        {"name": "Day 1: Smoothie & Salad", "description": "Green smoothie and mixed veggie salad.", "calories": 400},
        {"name": "Day 2: Oatmeal & Tofu Stir Fry", "description": "Oatmeal for breakfast and tofu stir fry for lunch.", "calories": 450},
        {"name": "Day 3: Chickpea Salad & Lentil Soup", "description": "Protein-rich chickpea salad and lentil soup.", "calories": 500},
    ]

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