from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/plan', methods=['POST'])
def plan():
    # just fake data so you can test plan.html
    prefs = "Diet: vegetarian\nMeals per day: 3\nCalories: 1600–1800\nDislikes: peanuts"
    plan_md = "This is a sample meal plan.\n\n- Day 1: Smoothie + Salad\n- Day 2: Oatmeal + Tofu stir fry"
    return render_template('plan.html', prefs=prefs, plan_md=plan_md)

if __name__ == '__main__':
    app.run(debug=True)
