import unittest
# the purpose of this file is to test basic functionality using unittest

def userMealRestrictions(meal):
    # Simulate user meal restriction logic
    restricted_meals = ['vegan', 'vegetarian', 'gluten-free']
    if intolerences.lower() in restricted_meals:
        return True
    return False


# Unit tests for userMealRestrictions function
class TestMealRestrictions(unittest.TestCase):
    def test_vegan_restriction(self):
        self.assertTrue(userMealRestrictions('vegan'))

    def test_non_restricted_meal(self):
        self.assertFalse(userMealRestrictions('chicken'))

    def test_gluten_free_restriction(self):
        self.assertTrue(userMealRestrictions('gluten-free'))

    def test_empty_string(self):
        self.assertFalse(userMealRestrictions(''))

if __name__ == '__main__':
    unittest.main()