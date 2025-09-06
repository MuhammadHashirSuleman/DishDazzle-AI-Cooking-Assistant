import os
import sys
import unittest
from unittest.mock import patch, MagicMock

# Add the src directory to the path so we can import the modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PyQt5.QtWidgets import QApplication
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt

# Create a QApplication instance for testing
app = QApplication([])

from src.ui import MainWindow

class TestUI(unittest.TestCase):
    def setUp(self):
        # Create a mock for database functions
        self.db_patcher = patch('src.ui.get_all_recipes')
        self.mock_get_all_recipes = self.db_patcher.start()
        self.mock_get_all_recipes.return_value = [
            {
                "id": 1,
                "name": "Test Recipe",
                "ingredients": ["ingredient1", "ingredient2"],
                "instructions": ["step1", "step2"],
                "cooking_time": 30,
                "difficulty": "Easy",
                "image_url": "http://example.com/image.jpg"
            }
        ]
        
        # Create a mock for API functions
        self.api_patcher = patch('src.ui.get_recipe_suggestions')
        self.mock_get_recipe_suggestions = self.api_patcher.start()
        self.mock_get_recipe_suggestions.return_value = {
            "recipes": [
                {
                    "name": "Suggested Recipe",
                    "ingredients": ["ingredient1", "ingredient2"],
                    "instructions": ["step1", "step2"]
                }
            ]
        }
        
        # Create the main window
        self.window = MainWindow()
    
    def tearDown(self):
        # Stop the patchers
        self.db_patcher.stop()
        self.api_patcher.stop()
        
        # Close the window
        self.window.close()
    
    def test_window_title(self):
        # Test that the window title is set correctly
        self.assertEqual(self.window.windowTitle(), "DishDazzle")
    
    def test_tabs_exist(self):
        # Test that all tabs exist
        tab_widget = self.window.centralWidget().findChild(QTabWidget)
        self.assertIsNotNone(tab_widget)
        
        # Check that we have the expected number of tabs
        expected_tabs = 5  # Recipes, Suggestions, Assistant, Grocery/Pantry, Cooking
        self.assertEqual(tab_widget.count(), expected_tabs)
    
    @patch('src.ui.get_recipe_by_id')
    def test_recipe_loading(self, mock_get_recipe_by_id):
        # Mock the get_recipe_by_id function
        mock_get_recipe_by_id.return_value = {
            "id": 1,
            "name": "Test Recipe",
            "ingredients": ["ingredient1", "ingredient2"],
            "instructions": ["step1", "step2"],
            "cooking_time": 30,
            "difficulty": "Easy",
            "image_url": "http://example.com/image.jpg"
        }
        
        # Test that recipes are loaded into the recipe list
        recipe_list = self.window.recipe_list
        self.assertIsNotNone(recipe_list)
        
        # Check that the recipe list has items
        self.assertTrue(recipe_list.count() > 0)
        
        # Select the first recipe
        recipe_list.setCurrentRow(0)
        
        # Check that the recipe details are displayed
        self.assertEqual(self.window.recipe_name_label.text(), "Test Recipe")
    
    @patch('src.ui.add_to_grocery_list')
    def test_add_to_grocery_list(self, mock_add_to_grocery_list):
        # Test adding an item to the grocery list
        self.window.grocery_item_input.setText("Test Item")
        self.window.grocery_amount_input.setText("1 kg")
        
        # Click the add button
        QTest.mouseClick(self.window.add_grocery_btn, Qt.LeftButton)
        
        # Check that the add_to_grocery_list function was called
        mock_add_to_grocery_list.assert_called_once()
    
    @patch('src.ui.get_config')
    @patch('src.ui.update_config')
    def test_theme_toggle(self, mock_update_config, mock_get_config):
        # Mock the get_config function
        mock_get_config.return_value = {"theme": "light"}
        
        # Test toggling the theme
        self.window.toggle_theme()
        
        # Check that update_config was called with the new theme
        mock_update_config.assert_called_once_with({"theme": "dark"})

if __name__ == '__main__':
    unittest.main()