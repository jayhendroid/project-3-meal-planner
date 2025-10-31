# This file contains unit tests to verify that our meal planner app works correctly
# Unit tests check small pieces of code to make sure they behave as expected

import unittest
from unittest.mock import patch, MagicMock
import os
import importlib

# A simple helper function to test meal restriction logic
# This simulates checking if a food restriction matches our supported diets
def userMealRestrictions(intolerences):
    """Check if the given food restriction is one we support in our app.

    Args:
        intolerences: The food restriction to check (should be a string)

    Returns:
        True if it's a supported restriction, False otherwise
    """
    # First check if the input is actually a string
    if not isinstance(intolerences, str):
        return False

    # List of food restrictions we support in our meal planner
    restricted_meals = ['vegan', 'vegetarian', 'gluten-free']

    # Check if the input matches any of our supported restrictions (case-insensitive)
    if intolerences.lower() in restricted_meals:
        return True
    return False

# Test class for the userMealRestrictions function
class TestMealRestrictions(unittest.TestCase):
    """Test cases for the meal restriction checking function."""

    def test_valid_restriction(self):
        """Test that valid restrictions like 'vegan' return True."""
        self.assertTrue(userMealRestrictions('vegan'))

    def test_non_restricted_meal(self):
        """Test that unsupported foods like 'chicken' return False."""
        self.assertFalse(userMealRestrictions('chicken'))

    def test_empty_string(self):
        """Test that empty strings return False."""
        self.assertFalse(userMealRestrictions(''))

    def test_case_insensitivity(self):
        """Test that the check works regardless of uppercase/lowercase."""
        self.assertTrue(userMealRestrictions('Vegan'))

    def test_partial_match(self):
        """Test that partial matches like 'veg' don't count as full matches."""
        self.assertFalse(userMealRestrictions('veg'))

    def test_numeric_input(self):
        """Test that numbers as strings return False."""
        self.assertFalse(userMealRestrictions('1234'))

    def test_special_characters(self):
        """Test that special characters return False."""
        self.assertFalse(userMealRestrictions('@#$%'))

    def test_multiple_restrictions(self):
        """Test that multiple restrictions in one string return False."""
        self.assertFalse(userMealRestrictions('vegetarian, gluten-free'))

    def test_whitespace_input(self):
        """Test that strings with only spaces return False."""
        self.assertFalse(userMealRestrictions('   '))

    def test_none_input(self):
        """Test that None values return False."""
        self.assertFalse(userMealRestrictions(None))

    def test_long_string_input(self):
        """Test that very long strings return False."""
        long_string = 'a' * 1000
        self.assertFalse(userMealRestrictions(long_string))

    def test_dictionary_input(self):
        """Test that dictionary inputs return False."""
        self.assertFalse(userMealRestrictions({'diet': 'vegan'}))

    def test_list_input(self):
        """Test that list inputs return False."""
        self.assertFalse(userMealRestrictions(['vegan', 'vegetarian']))

    def test_boolean_input(self):
        """Test that boolean inputs return False."""
        self.assertFalse(userMealRestrictions(True))

# Try to import the Spoonacular API module
# If it's not available (dependencies not installed), we'll skip those tests
try:
    import Spoonacular_api
    SPOONACULAR_AVAILABLE = True
except ImportError:
    SPOONACULAR_AVAILABLE = False

# Test class for Spoonacular API functions (only runs if module is available)
@unittest.skipUnless(SPOONACULAR_AVAILABLE, "Spoonacular_api module not available (dependencies not installed)")
class TestSpoonacularAPI(unittest.TestCase):
    """Test cases for the Spoonacular recipe API functions."""

    def test_missing_api_key_raises(self):
        """Test that missing API key raises ExternalAPIError."""
        # Temporarily remove the API key from environment variables
        original = os.environ.pop('SPOONACULAR_API_KEY', None)
        try:
            # Reload the module to pick up the missing key
            importlib.reload(Spoonacular_api)
            # This should raise an ExternalAPIError because no API key is set
            with self.assertRaises(Spoonacular_api.ExternalAPIError):
                Spoonacular_api.get_diet_recipes_by_meal('salad', '', 500, 'vegan')
        finally:
            # Restore the original API key if there was one
            if original is not None:
                os.environ['SPOONACULAR_API_KEY'] = original
            # Reload the module again to restore normal behavior
            importlib.reload(importlib.import_module('Spoonacular_api'))

    def test_spoonacular_bad_response(self):
        """Test that bad HTTP responses are converted to ExternalAPIError."""
        # Create a mock response that simulates a server error
        mock_resp = MagicMock()
        mock_resp.raise_for_status.side_effect = Exception('HTTP 500')
        mock_resp.status_code = 500
        mock_resp.text = 'server error'

        # Use patch to replace the real API call with our mock
        with patch('Spoonacular_api.requests.get', return_value=mock_resp):
            # This should raise ExternalAPIError because of the bad response
            with self.assertRaises(Spoonacular_api.ExternalAPIError):
                Spoonacular_api.get_diet_recipes_by_meal('soup', '', 400, '')

# Test class for Gemini AI fallback behavior
class TestGeminiFallback(unittest.TestCase):
    """Test cases for Gemini AI error handling."""

    def test_gemini_unavailable_raises(self):
        """Test that calling Gemini when unavailable raises RuntimeError."""
        import Gemini

        # Save the original values so we can restore them later
        orig_genai = getattr(Gemini, 'genai', None)
        orig_model = getattr(Gemini, 'AImodel', None)

        # Temporarily set Gemini to None to simulate it being unavailable
        Gemini.genai = None
        Gemini.AImodel = None

        try:
            # This should raise RuntimeError because Gemini is not available
            with self.assertRaises(RuntimeError):
                Gemini.gemini_query('Make a recipe')
        finally:
            # Always restore the original values, even if the test fails
            Gemini.genai = orig_genai
            Gemini.AImodel = orig_model

# TODO: Add unit tests for Flask app routes
# TODO: Add unit tests for system_prompt function in Gemini.py
# TODO: Add unit tests for get_diet_recipes_by_meal function in Spoonacular_api.py
# TODO: Add unit tests for get_recipe_information function in Spoonacular_api.py
# TODO: Add unit test for JSON response parsing

# Additional unit tests can be added here as needed

# Run all the tests when this file is executed directly
if __name__ == '__main__':
    unittest.main()
