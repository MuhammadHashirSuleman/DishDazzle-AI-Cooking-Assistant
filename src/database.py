#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
DishDazzle - Database Module
Handles SQLite database operations for recipe management
"""

import os
import json
import sqlite3
import logging
from pathlib import Path

# Get logger
logger = logging.getLogger(__name__)

# Database file path
DB_PATH = Path(os.path.dirname(os.path.dirname(__file__))) / 'data' / 'dishdazzle.db'


def get_db_connection():
    """Create and return a database connection"""
    try:
        # Ensure data directory exists
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        
        # Create connection with row factory for dictionary-like results
        conn = sqlite3.connect(str(DB_PATH))
        conn.row_factory = sqlite3.Row
        
        return conn
    except sqlite3.Error as e:
        logger.error(f"Database connection error: {e}")
        raise


def initialize_database():
    """Initialize the database with required tables if they don't exist"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Create recipes table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS recipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            ingredients TEXT NOT NULL,  -- JSON string
            instructions TEXT NOT NULL,  -- JSON string
            cooking_time INTEGER,  -- in minutes
            difficulty TEXT CHECK(difficulty IN ('Easy', 'Medium', 'Hard')),
            image_url TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # Create favorites table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS favorites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            recipe_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (recipe_id) REFERENCES recipes (id) ON DELETE CASCADE
        )
        ''')
        
        # Create pantry table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS pantry (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ingredients TEXT NOT NULL,  -- JSON string
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # Create grocery_list table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS grocery_list (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            items TEXT NOT NULL,  -- JSON string
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        conn.commit()
        logger.info("Database initialized successfully")
        
        # Check if we need to add sample recipes
        cursor.execute("SELECT COUNT(*) FROM recipes")
        count = cursor.fetchone()[0]
        
        if count == 0:
            add_sample_recipes()
            
    except sqlite3.Error as e:
        logger.error(f"Database initialization error: {e}")
        raise
    finally:
        if conn:
            conn.close()


def add_sample_recipes():
    """Add sample recipes to the database"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Sample recipes
        sample_recipes = [
            {
                "name": "Pasta Aglio e Olio",
                "description": "A simple, classic Italian pasta dish with garlic and olive oil.",
                "ingredients": json.dumps([
                    {"name": "Spaghetti", "amount": "1 pound"},
                    {"name": "Olive oil", "amount": "1/2 cup"},
                    {"name": "Garlic", "amount": "6 cloves, thinly sliced"},
                    {"name": "Red pepper flakes", "amount": "1 teaspoon"},
                    {"name": "Parsley", "amount": "1/4 cup, chopped"},
                    {"name": "Salt", "amount": "To taste"},
                    {"name": "Black pepper", "amount": "To taste"}
                ]),
                "instructions": json.dumps([
                    "Bring a large pot of salted water to a boil.",
                    "Cook spaghetti according to package directions until al dente.",
                    "Meanwhile, heat olive oil in a large pan over medium heat.",
                    "Add sliced garlic and red pepper flakes, cooking until garlic is lightly golden.",
                    "Drain pasta, reserving 1/4 cup of pasta water.",
                    "Add pasta to the pan with garlic and oil, tossing to coat.",
                    "Add reserved pasta water if needed to loosen the sauce.",
                    "Season with salt and pepper, and garnish with chopped parsley."
                ]),
                "cooking_time": 20,
                "difficulty": "Easy",
                "image_url": "https://example.com/pasta_aglio_olio.jpg"
            },
            {
                "name": "Caprese Salad",
                "description": "A simple Italian salad made with fresh tomatoes, mozzarella, and basil.",
                "ingredients": json.dumps([
                    {"name": "Tomatoes", "amount": "4 large, sliced"},
                    {"name": "Fresh mozzarella", "amount": "16 oz, sliced"},
                    {"name": "Fresh basil leaves", "amount": "1 bunch"},
                    {"name": "Extra virgin olive oil", "amount": "1/4 cup"},
                    {"name": "Balsamic glaze", "amount": "2 tablespoons"},
                    {"name": "Salt", "amount": "To taste"},
                    {"name": "Black pepper", "amount": "To taste"}
                ]),
                "instructions": json.dumps([
                    "Arrange tomato and mozzarella slices alternately on a serving plate.",
                    "Tuck fresh basil leaves between the tomato and cheese slices.",
                    "Drizzle with olive oil and balsamic glaze.",
                    "Season with salt and freshly ground black pepper.",
                    "Serve immediately at room temperature."
                ]),
                "cooking_time": 10,
                "difficulty": "Easy",
                "image_url": "https://example.com/caprese_salad.jpg"
            },
            {
                "name": "Classic Beef Stew",
                "description": "A hearty beef stew with vegetables and rich gravy.",
                "ingredients": json.dumps([
                    {"name": "Beef chuck", "amount": "2 pounds, cubed"},
                    {"name": "Onions", "amount": "2 medium, chopped"},
                    {"name": "Carrots", "amount": "4 medium, chopped"},
                    {"name": "Potatoes", "amount": "4 medium, cubed"},
                    {"name": "Celery", "amount": "3 stalks, chopped"},
                    {"name": "Garlic", "amount": "3 cloves, minced"},
                    {"name": "Beef broth", "amount": "4 cups"},
                    {"name": "Tomato paste", "amount": "2 tablespoons"},
                    {"name": "Flour", "amount": "1/4 cup"},
                    {"name": "Vegetable oil", "amount": "3 tablespoons"},
                    {"name": "Bay leaves", "amount": "2"},
                    {"name": "Thyme", "amount": "1 teaspoon"},
                    {"name": "Salt", "amount": "To taste"},
                    {"name": "Black pepper", "amount": "To taste"}
                ]),
                "instructions": json.dumps([
                    "Season beef with salt and pepper, then coat with flour.",
                    "Heat oil in a large pot over medium-high heat.",
                    "Brown beef in batches, then set aside.",
                    "In the same pot, sauté onions, carrots, and celery until softened.",
                    "Add garlic and cook for 1 minute.",
                    "Stir in tomato paste and cook for 2 minutes.",
                    "Return beef to the pot and add beef broth, bay leaves, and thyme.",
                    "Bring to a boil, then reduce heat and simmer covered for 1.5 hours.",
                    "Add potatoes and simmer for another 30-45 minutes until meat and vegetables are tender.",
                    "Season with additional salt and pepper if needed."
                ]),
                "cooking_time": 150,
                "difficulty": "Medium",
                "image_url": "https://example.com/beef_stew.jpg"
            }
        ]
        
        # Insert sample recipes
        for recipe in sample_recipes:
            cursor.execute('''
            INSERT INTO recipes (name, description, ingredients, instructions, cooking_time, difficulty, image_url)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                recipe["name"],
                recipe["description"],
                recipe["ingredients"],
                recipe["instructions"],
                recipe["cooking_time"],
                recipe["difficulty"],
                recipe["image_url"]
            ))
        
        # Initialize empty pantry
        cursor.execute('''
        INSERT INTO pantry (ingredients) VALUES (?)
        ''', (json.dumps([]),))
        
        # Initialize empty grocery list
        cursor.execute('''
        INSERT INTO grocery_list (items) VALUES (?)
        ''', (json.dumps([]),))
        
        conn.commit()
        logger.info("Sample recipes added successfully")
        
    except sqlite3.Error as e:
        logger.error(f"Error adding sample recipes: {e}")
        raise
    finally:
        if conn:
            conn.close()


def get_all_recipes():
    """Get all recipes from the database"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM recipes ORDER BY name")
        recipes = cursor.fetchall()
        
        # Convert to list of dictionaries
        result = []
        for recipe in recipes:
            recipe_dict = dict(recipe)
            recipe_dict['ingredients'] = json.loads(recipe_dict['ingredients'])
            recipe_dict['instructions'] = json.loads(recipe_dict['instructions'])
            result.append(recipe_dict)
            
        return result
        
    except sqlite3.Error as e:
        logger.error(f"Error getting recipes: {e}")
        raise
    finally:
        if conn:
            conn.close()


def get_recipe_by_id(recipe_id):
    """Get a recipe by its ID"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM recipes WHERE id = ?", (recipe_id,))
        recipe = cursor.fetchone()
        
        if recipe:
            recipe_dict = dict(recipe)
            recipe_dict['ingredients'] = json.loads(recipe_dict['ingredients'])
            recipe_dict['instructions'] = json.loads(recipe_dict['instructions'])
            return recipe_dict
        else:
            return None
        
    except sqlite3.Error as e:
        logger.error(f"Error getting recipe by ID: {e}")
        raise
    finally:
        if conn:
            conn.close()


def search_recipes(query):
    """Search recipes by name or description"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Use LIKE for case-insensitive search
        search_term = f"%{query}%"
        cursor.execute(
            "SELECT * FROM recipes WHERE name LIKE ? OR description LIKE ? ORDER BY name",
            (search_term, search_term)
        )
        recipes = cursor.fetchall()
        
        # Convert to list of dictionaries
        result = []
        for recipe in recipes:
            recipe_dict = dict(recipe)
            recipe_dict['ingredients'] = json.loads(recipe_dict['ingredients'])
            recipe_dict['instructions'] = json.loads(recipe_dict['instructions'])
            result.append(recipe_dict)
            
        return result
        
    except sqlite3.Error as e:
        logger.error(f"Error searching recipes: {e}")
        raise
    finally:
        if conn:
            conn.close()


def add_recipe(recipe_data):
    """Add a new recipe to the database"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Ensure ingredients and instructions are JSON strings
        if isinstance(recipe_data['ingredients'], list):
            recipe_data['ingredients'] = json.dumps(recipe_data['ingredients'])
            
        if isinstance(recipe_data['instructions'], list):
            recipe_data['instructions'] = json.dumps(recipe_data['instructions'])
        
        cursor.execute('''
        INSERT INTO recipes (name, description, ingredients, instructions, cooking_time, difficulty, image_url)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            recipe_data["name"],
            recipe_data.get("description", ""),
            recipe_data["ingredients"],
            recipe_data["instructions"],
            recipe_data.get("cooking_time", 0),
            recipe_data.get("difficulty", "Medium"),
            recipe_data.get("image_url", "")
        ))
        
        # Get the ID of the newly inserted recipe
        recipe_id = cursor.lastrowid
        
        conn.commit()
        logger.info(f"Recipe '{recipe_data['name']}' added successfully with ID {recipe_id}")
        
        return recipe_id
        
    except sqlite3.Error as e:
        logger.error(f"Error adding recipe: {e}")
        raise
    finally:
        if conn:
            conn.close()


def update_recipe(recipe_id, recipe_data):
    """Update an existing recipe"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Ensure ingredients and instructions are JSON strings
        if isinstance(recipe_data.get('ingredients'), list):
            recipe_data['ingredients'] = json.dumps(recipe_data['ingredients'])
            
        if isinstance(recipe_data.get('instructions'), list):
            recipe_data['instructions'] = json.dumps(recipe_data['instructions'])
        
        cursor.execute('''
        UPDATE recipes SET 
            name = ?,
            description = ?,
            ingredients = ?,
            instructions = ?,
            cooking_time = ?,
            difficulty = ?,
            image_url = ?
        WHERE id = ?
        ''', (
            recipe_data["name"],
            recipe_data.get("description", ""),
            recipe_data["ingredients"],
            recipe_data["instructions"],
            recipe_data.get("cooking_time", 0),
            recipe_data.get("difficulty", "Medium"),
            recipe_data.get("image_url", ""),
            recipe_id
        ))
        
        conn.commit()
        logger.info(f"Recipe with ID {recipe_id} updated successfully")
        
        return cursor.rowcount > 0  # Return True if a row was updated
        
    except sqlite3.Error as e:
        logger.error(f"Error updating recipe: {e}")
        raise
    finally:
        if conn:
            conn.close()


def delete_recipe(recipe_id):
    """Delete a recipe by its ID"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM recipes WHERE id = ?", (recipe_id,))
        
        conn.commit()
        logger.info(f"Recipe with ID {recipe_id} deleted successfully")
        
        return cursor.rowcount > 0  # Return True if a row was deleted
        
    except sqlite3.Error as e:
        logger.error(f"Error deleting recipe: {e}")
        raise
    finally:
        if conn:
            conn.close()


def add_to_favorites(recipe_id):
    """Add a recipe to favorites"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if already in favorites
        cursor.execute("SELECT id FROM favorites WHERE recipe_id = ?", (recipe_id,))
        if cursor.fetchone():
            logger.info(f"Recipe with ID {recipe_id} is already in favorites")
            return False
        
        cursor.execute("INSERT INTO favorites (recipe_id) VALUES (?)", (recipe_id,))
        
        conn.commit()
        logger.info(f"Recipe with ID {recipe_id} added to favorites")
        
        return True
        
    except sqlite3.Error as e:
        logger.error(f"Error adding to favorites: {e}")
        raise
    finally:
        if conn:
            conn.close()


def remove_from_favorites(recipe_id):
    """Remove a recipe from favorites"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM favorites WHERE recipe_id = ?", (recipe_id,))
        
        conn.commit()
        logger.info(f"Recipe with ID {recipe_id} removed from favorites")
        
        return cursor.rowcount > 0  # Return True if a row was deleted
        
    except sqlite3.Error as e:
        logger.error(f"Error removing from favorites: {e}")
        raise
    finally:
        if conn:
            conn.close()


def get_favorite_recipes():
    """Get all favorite recipes"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT r.* FROM recipes r
        JOIN favorites f ON r.id = f.recipe_id
        ORDER BY r.name
        ''')
        recipes = cursor.fetchall()
        
        # Convert to list of dictionaries
        result = []
        for recipe in recipes:
            recipe_dict = dict(recipe)
            recipe_dict['ingredients'] = json.loads(recipe_dict['ingredients'])
            recipe_dict['instructions'] = json.loads(recipe_dict['instructions'])
            result.append(recipe_dict)
            
        return result
        
    except sqlite3.Error as e:
        logger.error(f"Error getting favorite recipes: {e}")
        raise
    finally:
        if conn:
            conn.close()


def get_pantry_ingredients():
    """Get the current pantry ingredients"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT ingredients FROM pantry LIMIT 1")
        result = cursor.fetchone()
        
        if result:
            return json.loads(result['ingredients'])
        else:
            # Initialize pantry if it doesn't exist
            cursor.execute("INSERT INTO pantry (ingredients) VALUES (?)", (json.dumps([]),))
            conn.commit()
            return []
        
    except sqlite3.Error as e:
        logger.error(f"Error getting pantry ingredients: {e}")
        raise
    finally:
        if conn:
            conn.close()


def update_pantry_ingredients(ingredients):
    """Update the pantry ingredients"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Ensure ingredients is a JSON string
        if isinstance(ingredients, list):
            ingredients = json.dumps(ingredients)
        
        cursor.execute("SELECT id FROM pantry LIMIT 1")
        result = cursor.fetchone()
        
        if result:
            cursor.execute("UPDATE pantry SET ingredients = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?", 
                          (ingredients, result['id']))
        else:
            cursor.execute("INSERT INTO pantry (ingredients) VALUES (?)", (ingredients,))
        
        conn.commit()
        logger.info("Pantry ingredients updated successfully")
        
        return True
        
    except sqlite3.Error as e:
        logger.error(f"Error updating pantry ingredients: {e}")
        raise
    finally:
        if conn:
            conn.close()


def get_grocery_list():
    """Get the current grocery list"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT items FROM grocery_list LIMIT 1")
        result = cursor.fetchone()
        
        if result:
            return json.loads(result['items'])
        else:
            # Initialize grocery list if it doesn't exist
            cursor.execute("INSERT INTO grocery_list (items) VALUES (?)", (json.dumps([]),))
            conn.commit()
            return []
        
    except sqlite3.Error as e:
        logger.error(f"Error getting grocery list: {e}")
        raise
    finally:
        if conn:
            conn.close()


def update_grocery_list(items):
    """Update the grocery list"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Ensure items is a JSON string
        if isinstance(items, list):
            items = json.dumps(items)
        
        cursor.execute("SELECT id FROM grocery_list LIMIT 1")
        result = cursor.fetchone()
        
        if result:
            cursor.execute("UPDATE grocery_list SET items = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?", 
                          (items, result['id']))
        else:
            cursor.execute("INSERT INTO grocery_list (items) VALUES (?)", (items,))
        
        conn.commit()
        logger.info("Grocery list updated successfully")
        
        return True
        
    except sqlite3.Error as e:
        logger.error(f"Error updating grocery list: {e}")
        raise
    finally:
        if conn:
            conn.close()