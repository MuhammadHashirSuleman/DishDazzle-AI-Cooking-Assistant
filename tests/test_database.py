import os
import sys
import unittest
import tempfile

# Add the src directory to the path so we can import the modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.database import (
    init_db, create_tables, get_all_recipes, add_recipe, 
    get_recipe_by_id, update_recipe, delete_recipe
)

class TestDatabase(unittest.TestCase):
    def setUp(self):
        # Create a temporary database file
        self.db_fd, self.db_path = tempfile.mkstemp()
        # Initialize the database with the temporary file
        init_db(self.db_path)
        create_tables()
        
    def tearDown(self):
        # Close and remove the temporary database
        os.close(self.db_fd)
        os.unlink(self.db_path)
    
    def test_add_and_get_recipe(self):
        # Test adding a recipe
        recipe = {
            "name": "Test Recipe",
            "ingredients": ["ingredient1", "ingredient2"],
            "instructions": ["step1", "step2"],
            "cooking_time": 30,
            "difficulty": "Easy",
            "image_url": "http://example.com/image.jpg"
        }
        
        # Add the recipe
        recipe_id = add_recipe(recipe)
        
        # Verify it was added
        self.assertIsNotNone(recipe_id)
        
        # Get the recipe by ID
        retrieved_recipe = get_recipe_by_id(recipe_id)
        
        # Verify the retrieved recipe matches what we added
        self.assertEqual(retrieved_recipe["name"], recipe["name"])
        self.assertEqual(retrieved_recipe["cooking_time"], recipe["cooking_time"])
        self.assertEqual(retrieved_recipe["difficulty"], recipe["difficulty"])
    
    def test_get_all_recipes(self):
        # Add multiple recipes
        recipes = [
            {
                "name": "Recipe 1",
                "ingredients": ["ingredient1", "ingredient2"],
                "instructions": ["step1", "step2"],
                "cooking_time": 30,
                "difficulty": "Easy",
                "image_url": "http://example.com/image1.jpg"
            },
            {
                "name": "Recipe 2",
                "ingredients": ["ingredient3", "ingredient4"],
                "instructions": ["step1", "step2"],
                "cooking_time": 45,
                "difficulty": "Medium",
                "image_url": "http://example.com/image2.jpg"
            }
        ]
        
        for recipe in recipes:
            add_recipe(recipe)
        
        # Get all recipes
        all_recipes = get_all_recipes()
        
        # Verify we got the correct number of recipes
        self.assertEqual(len(all_recipes), len(recipes))
    
    def test_update_recipe(self):
        # Add a recipe
        recipe = {
            "name": "Original Recipe",
            "ingredients": ["ingredient1", "ingredient2"],
            "instructions": ["step1", "step2"],
            "cooking_time": 30,
            "difficulty": "Easy",
            "image_url": "http://example.com/image.jpg"
        }
        
        recipe_id = add_recipe(recipe)
        
        # Update the recipe
        updated_recipe = {
            "id": recipe_id,
            "name": "Updated Recipe",
            "ingredients": ["ingredient1", "ingredient2", "ingredient3"],
            "instructions": ["step1", "step2", "step3"],
            "cooking_time": 45,
            "difficulty": "Medium",
            "image_url": "http://example.com/updated_image.jpg"
        }
        
        update_recipe(updated_recipe)
        
        # Get the updated recipe
        retrieved_recipe = get_recipe_by_id(recipe_id)
        
        # Verify the update was successful
        self.assertEqual(retrieved_recipe["name"], updated_recipe["name"])
        self.assertEqual(retrieved_recipe["cooking_time"], updated_recipe["cooking_time"])
        self.assertEqual(retrieved_recipe["difficulty"], updated_recipe["difficulty"])
    
    def test_delete_recipe(self):
        # Add a recipe
        recipe = {
            "name": "Recipe to Delete",
            "ingredients": ["ingredient1", "ingredient2"],
            "instructions": ["step1", "step2"],
            "cooking_time": 30,
            "difficulty": "Easy",
            "image_url": "http://example.com/image.jpg"
        }
        
        recipe_id = add_recipe(recipe)
        
        # Verify it was added
        self.assertIsNotNone(get_recipe_by_id(recipe_id))
        
        # Delete the recipe
        delete_recipe(recipe_id)
        
        # Verify it was deleted
        self.assertIsNone(get_recipe_by_id(recipe_id))

if __name__ == '__main__':
    unittest.main()