import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv("KEYS.env")
api_key = os.getenv("GOOGLE_AI_KEY")

if not api_key:
    raise ValueError("Missing GOOGLE_AI_KEY in KEYS.env")

# Configure Gemini API
genai.configure(api_key=api_key)


# Get a model that supports generate_content
def get_available_model():
    models = genai.list_models()
    for m in models:
        if "gemini" in m.name and "embedding" not in m.name:
            if "generateContent" in m.supported_generation_methods:
                print(f"Using model: {m.name}")
                return genai.GenerativeModel(m.name)
    raise RuntimeError("No suitable Gemini model found for content generation.")


# Initialize AI model
AImodel = get_available_model()


# Generate text safely
def gemini_query(prompt):
    try:
        response = AImodel.generate_content(
            prompt,
            generation_config={
                "max_output_tokens": 4000,  # increased from 2000
                "temperature": 0.7,
                "top_p": 0.9,
            },
        )

        # Ensure we have at least one candidate
        if not response or not hasattr(response, 'candidates') or not response.candidates:
            return "Gemini API returned no content."

        candidate = response.candidates[0]

        # Extract text safely
        content = getattr(candidate, 'content', None)
        if content:
            # If 'parts' exist, join all part.text
            parts = getattr(content, 'parts', None)
            if parts:
                text_parts = [getattr(part, 'text', '').strip() for part in parts if getattr(part, 'text', '').strip()]
                if text_parts:
                    return "\n".join(text_parts)
            # Fallback: direct text field
            text = getattr(content, 'text', None)
            if text and text.strip():
                return text.strip()

        # Last resort: convert candidate to string
        return str(candidate)

    except Exception as e:
        print("Gemini API error:", e)
        return "Gemini API quota exceeded or unavailable. Please try again later."


# Structure recipe information
def recipe_info(diet, intolerances, calorieTarget, recipe_info_list):
    return {
        'diet': diet,
        'intolerances': intolerances,
        'calorieTarget': calorieTarget,
        'recipes': recipe_info_list
    }


# Format user input for Gemini prompt (simplified)
def user_prompt(user_input):
    recipes_summary = []
    for r in user_input['recipes']:
        title = r.get('title', 'Unknown recipe')
        ingredients = r.get('ingredients', [])
        # Keep it short: only include top 5 ingredients
        ingredients_list = ", ".join(ingredients[:5])
        recipes_summary.append(f"{title}: {ingredients_list}")

    recipes_text = "\n".join(recipes_summary)

    return f"""User dietary preferences:
Diet: {user_input['diet']}
Intolerances: {user_input['intolerances']}
Calorie Target: {user_input['calorieTarget']}

Use the following recipes as inspiration (only titles + main ingredients):
{recipes_text}

Generate a detailed recipe with step-by-step instructions for this user."""


# System prompt with instructions for Gemini
def system_prompt():
    return """Using the meal data provided by the user, generate a detailed dietary recipe 
with step-by-step instructions, catering to the user's dietary strategy, intolerances, and calorie target.
Use the recipes provided by the user data as inspiration."""
