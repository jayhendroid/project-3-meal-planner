# This file creates a web application for meal planning using Flask
# It lets users enter their preferences and generates a meal plan

import logging
from flask import Flask, render_template, request
from Spoonacular_api import get_diet_recipes_by_meal, ExternalAPIError
from Gemini import user_prompt

# Set up logging so we can see what's happening when the app runs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create the main Flask application object
app = Flask(__name__)

# This route shows the home page where users enter their preferences
@app.route('/') # home page route
def home():
    return render_template('index.html')

# This route handles the form submission and creates the meal plan
@app.route('/plan', methods=['POST'])
def plan():
    try:
        # Get the user's diet choice from the form (defaults to omnivore if not selected)
        diet = request.form.get('diet', 'omnivore')

        # Check that the user entered a valid number of meals per day
        meals_per_day_str = request.form.get('meals_per_day', '').strip()
        if not meals_per_day_str:
            # User didn't enter anything, so show an error message
            return render_template('error.html', error_message="Please enter the number of meals per day (2-5)."), 400

        try:
            # Try to convert the text to a number
            meals_per_day = int(meals_per_day_str)
            if meals_per_day < 2 or meals_per_day > 5:
                # Number is outside our allowed range
                return render_template('error.html', error_message="Meals per day must be between 2 and 5."), 400
        except ValueError:
            # User entered something that isn't a number
            return render_template('error.html', error_message="Please enter a valid number for meals per day (2-5)."), 400

        # Get the other form fields (these are optional)
        calories = request.form.get('calories', '').strip()
        dislikes = request.form.get('dislikes', '').strip()

        # Special test cases for checking error handling (remove these in production)
        if diet == 'error_test':
            raise ExternalAPIError("Simulated API error for testing")
        if diet == 'runtime_test':
            raise RuntimeError("Simulated Gemini API error for testing")

        # For now, just show fake sample data instead of real meal plans
        # This will be replaced with actual API calls later
        prefs = f"Diet: {diet}\nMeals per day: {meals_per_day}\nCalories: {calories}\nDislikes: {dislikes}"
        plan_md = "This is a sample meal plan.\n\n- Day 1: Smoothie + Salad\n- Day 2: Oatmeal + Tofu stir fry"
        return render_template('plan.html', prefs=prefs, plan_md=plan_md)

    # Handle different types of errors that might occur
    except ExternalAPIError as e:
        # Something went wrong with the recipe API
        logger.error("External API error in /plan: %s", e)
        return render_template('error.html', error_message="We're having trouble generating your meal plan right now. Please try again later."), 503
    except RuntimeError as e:
        # Something went wrong with the AI text generation
        logger.error("Gemini API error in /plan: %s", e)
        return render_template('error.html', error_message="We're having trouble generating your meal plan right now. Please try again later."), 503
    except Exception as e:
        # Any other unexpected error
        logger.exception("Unexpected error in /plan: %s", e)
        return render_template('error.html', error_message="An unexpected error occurred. Please try again."), 500

# This handles any internal server errors (500 errors)
@app.errorhandler(500)
def internal_error(error):
    logger.exception("Internal server error: %s", error)
    return render_template('error.html', error_message="An internal server error occurred. Please try again."), 500

# This handles requests to pages that don't exist (404 errors)
@app.errorhandler(404)
def not_found_error(error):
    return render_template('error.html', error_message="Page not found."), 404

# Only run the app if this file is executed directly (not imported)
if __name__ == '__main__':
    app.run(debug=True)
