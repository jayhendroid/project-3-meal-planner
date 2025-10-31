# This file handles communication with Google's Gemini AI service
# It uses AI to create detailed meal recipes based on user preferences and recipe data

import os
import logging

# Try to import the Google Gemini library
# If it's not installed, we'll set genai to None so the app can still work without AI features
try:
    import google.generativeai as genai
except ImportError:
    # genai == None tells the rest of the app that Gemini features are not available
    genai = None

logger = logging.getLogger(__name__)

# Set up the Gemini AI model if the library is available and we have an API key
# This happens when the module is first loaded
if genai is not None:
    # Only configure if we have the API key in environment variables
    api_key = os.environ.get("GOOGLE_API_KEY")
    if api_key:
        genai.configure(api_key=api_key)
        # Create the AI model object we can use to generate text
        AImodel = genai.GenerativeModel(model_name="gemini-2.0-flash-exp")
    else:
        logger.warning("GOOGLE_API_KEY not set; Gemini features will be disabled.")
        AImodel = None
else:
    logger.warning("google.generativeai not installed; Gemini features will be disabled.")

# Function to ask Gemini AI to generate text based on a prompt
def gemini_query(prompt):
    """Send a prompt to Gemini AI and get back generated text.

    This function takes a text prompt (like instructions for creating a recipe)
    and sends it to Google's Gemini AI service. The AI generates a response
    based on the prompt.

    Args:
        prompt: The text instructions for what you want the AI to generate

    Returns:
        The AI-generated text response

    Raises:
        RuntimeError: If Gemini is not available (missing library or API key)
    """

    # Check if Gemini is ready to use
    if genai is None or AImodel is None:
        raise RuntimeError(
            "Gemini client is not available. Ensure 'google-generativeai' is installed "
            "and GOOGLE_API_KEY is set in the environment."
        )

    # Send the prompt to Gemini and get the response
    response = AImodel.generate_content(
        contents=prompt,
        generation_config={
            "max_output_tokens": 500,  # Limit response length
            "temperature": 0.7,  # How creative/random the response should be (0.0-1.0)
            "top_p": 0.9,  # Another creativity control setting
        }
    )
    return response.text

# Function to organize recipe information into a structured format
def recipe_info(meal, intolerances, diet, calorieTarget, recipe_info_list):
    """Create a structured dictionary containing all the meal planning information.

    This takes separate pieces of information about a meal and puts them together.
    """
    meal_data = {
        'meal': meal,
        'intolerances': intolerances,
        'diet': diet,
        'calorieTarget': calorieTarget,
        'recipes': recipe_info_list
    }
    return meal_data

# Function to format user preferences and recipe data into a prompt for the AI
def user_prompt(user_input):
    """Convert meal planning data into a formatted text prompt for Gemini AI.
    """
    Meal_Data = f"""Meal: {user_input['meal']}
Intolerances: {user_input['intolerances']}
Diet: {user_input['diet']}
Calorie Target: {user_input['calorieTarget']}
Recipes: {user_input['recipes']}
"""
    return Meal_Data

# Function to create instructions for the AI about how to generate recipes
def system_prompt():
    """Create the system instructions that tell Gemini AI how to generate recipes.

    This provides the AI with clear guidelines about what kind of recipes to create,
    what to consider (diet, allergies, calories), and how to format the response.
    """
    prompt = f"""Using the meal data provided by the user, generate a detailed meal recipe
    with step by step instructions, catering to the user's dietary preferences, intolerances, and calorie target.
    Use the recipes provided by the user data as inspiration."""
    return prompt

