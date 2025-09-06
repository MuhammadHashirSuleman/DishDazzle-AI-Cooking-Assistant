import os
import sys
import unittest
from unittest.mock import patch, MagicMock

# Add the src directory to the path so we can import the modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.api import (
    init_api, get_recipe_suggestions, get_ingredient_substitutions,
    get_cooking_assistance, get_chat_response
)

class TestAPI(unittest.TestCase):
    @patch('src.api.openai.ChatCompletion.create')
    def test_get_recipe_suggestions(self, mock_create):
        # Mock the OpenAI API response
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message = {'content': '{"recipes": [{"name": "Pasta", "ingredients": ["pasta", "sauce"], "instructions": ["cook pasta", "add sauce"]}]}'}
        mock_create.return_value = mock_response
        
        # Call the function with test ingredients
        result = get_recipe_suggestions(["pasta", "sauce"])
        
        # Verify the result
        self.assertIsNotNone(result)
        self.assertIn("recipes", result)
        self.assertEqual(len(result["recipes"]), 1)
        self.assertEqual(result["recipes"][0]["name"], "Pasta")
    
    @patch('src.api.openai.ChatCompletion.create')
    def test_get_ingredient_substitutions(self, mock_create):
        # Mock the OpenAI API response
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message = {'content': '{"substitutions": [{"original": "butter", "substitute": "margarine"}]}'}
        mock_create.return_value = mock_response
        
        # Call the function with test ingredient
        result = get_ingredient_substitutions("butter")
        
        # Verify the result
        self.assertIsNotNone(result)
        self.assertIn("substitutions", result)
        self.assertEqual(len(result["substitutions"]), 1)
        self.assertEqual(result["substitutions"][0]["original"], "butter")
        self.assertEqual(result["substitutions"][0]["substitute"], "margarine")
    
    @patch('src.api.openai.ChatCompletion.create')
    def test_get_cooking_assistance(self, mock_create):
        # Mock the OpenAI API response
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message = {'content': 'Chop the onions finely and sauté them until translucent.'}
        mock_create.return_value = mock_response
        
        # Call the function with test question and context
        result = get_cooking_assistance("How do I chop onions?", "Recipe: Pasta with Onions\nCurrent step: Prepare the onions")
        
        # Verify the result
        self.assertIsNotNone(result)
        self.assertIn("Chop the onions", result)
    
    @patch('src.api.openai.ChatCompletion.create')
    def test_get_chat_response(self, mock_create):
        # Mock the OpenAI API response
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message = {'content': 'You can substitute milk with almond milk in most recipes.'}
        mock_create.return_value = mock_response
        
        # Call the function with test message
        result = get_chat_response("What can I use instead of milk?")
        
        # Verify the result
        self.assertIsNotNone(result)
        self.assertIn("almond milk", result)
    
    @patch('src.api.get_config')
    def test_init_api(self, mock_get_config):
        # Mock the config
        mock_get_config.return_value = {
            "api": {
                "openai_api_key": "test_key",
                "model": "gpt-3.5-turbo"
            }
        }
        
        # Call the function
        init_api()
        
        # No assertion needed as we're just testing that it doesn't raise an exception

if __name__ == '__main__':
    unittest.main()