import unittest
from unittest.mock import patch, MagicMock
import os
import json

# Set fake API keys for testing
os.environ["GOOGLE_API_KEY"] = "test_key"
os.environ["SPOONACULAR_API_KEY"] = "test_key"

from App import app
from Gemini import system_prompt
from Spoonacular_api import get_diet_recipes_by_diet, get_recipe_information


# userMealRestrictions function
def userMealRestrictions(intolerences):
    restricted_meals = ['vegan', 'vegetarian', 'gluten-free']

    if not isinstance(intolerences, str):
        return False

    intolerences = intolerences.strip().lower()
    if not intolerences:
        return False

    for restriction in restricted_meals:
        if restriction in intolerences.split(','):
            return True
    for restriction in restricted_meals:
        if restriction in intolerences:
            return True

    return False


# Unit tests for userMealRestrictions
class TestMealRestrictions(unittest.TestCase):
    def test_valid_restriction(self):
        self.assertTrue(userMealRestrictions('vegan'))

    def test_non_restricted_meal(self):
        self.assertFalse(userMealRestrictions('chicken'))

    def test_empty_string(self):
        self.assertFalse(userMealRestrictions(''))

    def test_case_insensitivity(self):
        self.assertTrue(userMealRestrictions('Vegan'))

    def test_multiple_restrictions(self):
        self.assertTrue(userMealRestrictions('vegetarian, gluten-free'))

    def test_none_input(self):
        self.assertFalse(userMealRestrictions(None))

    def test_numeric_input(self):
        self.assertFalse(userMealRestrictions(123))

    def test_list_input(self):
        self.assertFalse(userMealRestrictions([]))

    def test_dictionary_input(self):
        self.assertFalse(userMealRestrictions({}))

    def test_boolean_input(self):
        self.assertFalse(userMealRestrictions(True))


# Unit tests for Flask routes
class TestFlaskRoutes(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_home_route(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Recipe Results', response.data)

    def test_plan_route(self):
        response = self.app.post('/plan', data={
            'diet': '',
            'restrictions': '',
            'target_calories': ''
        })
        self.assertIn(response.status_code, [200, 302])


# Unit tests for Gemini
class TestGeminiFunctions(unittest.TestCase):
    def test_system_prompt_output(self):
        result = system_prompt()
        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 0)


# Unit tests for Spoonacular API
class TestSpoonacularAPI(unittest.TestCase):
    @patch('Spoonacular_api.requests.get')
    def test_get_diet_recipes_by_diet(self, mock_get):
        # Mock API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'results': [{'id': 1, 'title': 'Test Recipe'}]}
        mock_get.return_value = mock_response

        recipes, error = get_diet_recipes_by_diet('vegan', '', 2000)
        self.assertIsInstance(recipes, dict)
        self.assertIsNone(error)
        self.assertIn('results', recipes)
        self.assertEqual(recipes['results'][0]['title'], 'Test Recipe')

    def test_get_recipe_information(self):
        # Provide a list of dicts with all keys expected by the function
        mock_json = [{'id': 1, 'title': 'Test Recipe', 'calories': 100}]
        result = get_recipe_information(mock_json)
        self.assertIsInstance(result, list)
        self.assertEqual(result[0]['title'], 'Test Recipe')
        self.assertEqual(result[0]['id'], 1)
        self.assertEqual(result[0]['calories'], 100)


# Unit test for JSON parsing
class TestJSONParsing(unittest.TestCase):
    def test_parse_json_response(self):
        json_data = '{"results":[{"id":1,"title":"Recipe 1"}]}'
        parsed = json.loads(json_data)
        self.assertIsInstance(parsed, dict)
        self.assertIn('results', parsed)
        self.assertEqual(parsed['results'][0]['title'], 'Recipe 1')


if __name__ == '__main__':
    unittest.main()
