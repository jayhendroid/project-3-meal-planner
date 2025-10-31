# This file handles communication with the Spoonacular recipe API
# It gets recipe suggestions based on user preferences like diet and calories

import logging
import os
from typing import List, Dict

import requests
from requests import Response
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

logger = logging.getLogger(__name__)

# Get the API key from environment variables and set the API endpoint URL
# The app needs this key to work with Spoonacular - it's like a password for their service
API_KEY = os.getenv("SPOONACULAR_API_KEY")
URL = "https://api.spoonacular.com/recipes/complexSearch"


class ExternalAPIError(RuntimeError):
    """Custom error type for when the external recipe API fails.

    This lets the main app catch API problems separately from other errors,
    so it can show user-friendly messages instead of crashing.
    """


def _raise_for_status(resp: Response):
    """Check if the API response was successful, and if not, create a helpful error.

    This function looks at the HTTP response code. If it's not a success code
    it logs the problem and raises our custom ExternalAPIError so the app can handle it.
    """
    try:
        resp.raise_for_status()
    except requests.HTTPError as e:
        logger.error("Spoonacular API HTTP error %s: %s", resp.status_code, resp.text)
        raise ExternalAPIError(f"Spoonacular API error: {resp.status_code}") from e


@retry(
    retry=retry_if_exception_type((requests.exceptions.Timeout, requests.exceptions.ConnectionError)),
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=8),
)
def get_diet_recipes_by_meal(meal: str, intolerances: str, calorieTarget: int, diet: str) -> List[Dict]:
    """Get recipe suggestions from Spoonacular API based on meal preferences.
    """

    # Make sure we have the required API key
    if not API_KEY:
        logger.error("Missing SPOONACULAR_API_KEY environment variable")
        raise ExternalAPIError("Missing SPOONACULAR_API_KEY")

    # Set up the search parameters for the API request
    params = {
    'apiKey': API_KEY,
    'query': meal,  # What kind of meal we're looking for
    'maxCalories': calorieTarget,  # Don't exceed this calorie limit
    'diet': diet,  # Diet restriction like vegetarian/vegan
    'intolerances': intolerances,  # Foods to avoid
    'number': 5  # Get 5 recipe suggestions
    }

    try:
        # Make the API request with a timeout so it doesn't hang forever
        resp = requests.get(URL, params=params, timeout=8)
    except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
        # Network problems - let the retry decorator handle this
        logger.warning("Spoonacular request failed (retrying): %s", e)
        raise
    except Exception as e:
        # Some other unexpected error
        logger.exception("Unexpected error when calling Spoonacular: %s", e)
        raise ExternalAPIError("Unexpected error when calling Spoonacular") from e

    # Check if the API response was successful
    _raise_for_status(resp)

    try:
        # Convert the JSON response to a Python dictionary
        data = resp.json()
    except ValueError as e:
        # The response wasn't valid JSON
        logger.error("Invalid JSON from Spoonacular: %s", resp.text)
        raise ExternalAPIError("Invalid response from Spoonacular") from e

    # Extract the recipe results from the response
    results = data.get("results")
    if results is None:
        # The API response didn't have the expected "results" field
        logger.error("Spoonacular response missing 'results' key: %s", data)
        raise ExternalAPIError("Malformed response from Spoonacular")

    return results


# This function takes the raw API response and pulls out just the info we need
# It simplifies the complex API data into a cleaner format for our app
def get_recipe_information(json_response):
    """Extract important recipe details from the API response.
    """
    recipe_info_list = []
    for recipe in json_response:
        recipe_info = {
            'title': recipe.get('title'),  # Recipe name
            'id': recipe.get('id'),  # Unique recipe identifier
            'calories': recipe.get('calories', 'N/A')  # Calorie count, or N/A if not available
        }
        recipe_info_list.append(recipe_info)
    return recipe_info_list
