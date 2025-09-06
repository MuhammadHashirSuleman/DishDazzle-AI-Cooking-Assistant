#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
DishDazzle - API Module
Handles OpenRouter API integration for recipe suggestions and chatbot
"""

import json
import logging
import threading
from typing import List, Dict, Any, Optional, Callable

from openai import OpenAI

from utils import load_config

# Get logger
logger = logging.getLogger(__name__)

# API response cache
response_cache = {}
client = None

def initialize_api(model_type="deepseek"):
    """Initialize the OpenRouter API with the appropriate API key from config
    
    Args:
        model_type: Either "deepseek" or "llama" to specify which model to use
    """
    global client
    try:
        config = load_config()
        openrouter_config = config.get("api", {}).get("openrouter", {})
        
        if model_type == "deepseek":
            api_key = openrouter_config.get("deepseek", {}).get("api_key", "")
            model = openrouter_config.get("deepseek", {}).get("model", "deepseek/deepseek-v3.1")
        elif model_type == "llama":
            api_key = openrouter_config.get("llama", {}).get("api_key", "")
            model = openrouter_config.get("llama", {}).get("model", "meta-llama/llama-3-3-70b-instruct")
        else:
            logger.warning(f"Unknown model type: {model_type}")
            return False
        
        if not api_key:
            logger.warning(f"OpenRouter API key for {model_type} not found in config")
            return False
        
        # Configure OpenAI client to use OpenRouter
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )
        
        logger.info(f"OpenRouter API initialized successfully for {model_type} model: {model}")
        return True
        
    except Exception as e:
        logger.error(f"Error initializing API for {model_type}: {e}")
        return False

def get_recipe_suggestions(ingredients: List[str], callback: Optional[Callable] = None, model_type: str = "deepseek") -> Dict[str, Any]:
    """Get recipe suggestions based on available ingredients
    
    Args:
        ingredients: List of available ingredients
        callback: Optional callback function to receive the result asynchronously
        model_type: Either "deepseek" or "llama" to specify which model to use
        
    Returns:
        Dictionary with recipe suggestions if callback is None, otherwise None
    """
    # Create a cache key from the sorted ingredients
    cache_key = f"recipe_suggestions:{model_type}:" + ",".join(sorted(ingredients))
    
    # Check if we have a cached response
    if cache_key in response_cache:
        logger.info(f"Using cached recipe suggestions for {len(ingredients)} ingredients from {model_type}")
        result = response_cache[cache_key]
        
        if callback:
            callback(result)
            return None
        return result
    
    # Initialize API for the specified model
    if not initialize_api(model_type):
        error_msg = f"Failed to initialize API for {model_type}"
        logger.error(error_msg)
        result = {"recipes": [], "error": error_msg}
        
        if callback:
            callback(result)
            return None
        return result
    
    # If a callback is provided, run asynchronously
    if callback:
        thread = threading.Thread(
            target=_get_recipe_suggestions_async,
            args=(ingredients, cache_key, callback, model_type)
        )
        thread.daemon = True
        thread.start()
        return None
    
    # Otherwise, run synchronously
    return _get_recipe_suggestions_sync(ingredients, cache_key, model_type)

def _get_recipe_suggestions_sync(ingredients: List[str], cache_key: str, model_type: str) -> Dict[str, Any]:
    """Synchronous implementation of get_recipe_suggestions"""
    global client
    try:
        # Get config for model
        config = load_config()
        openrouter_config = config.get("api", {}).get("openrouter", {})
        
        if model_type == "deepseek":
            model = openrouter_config.get("deepseek", {}).get("model", "deepseek/deepseek-v3.1")
        else:
            model = openrouter_config.get("llama", {}).get("model", "meta-llama/llama-3-3-70b-instruct")
        
        # Prepare the prompt for the model
        prompt = f"""I have the following ingredients: {', '.join(ingredients)}.
        Please suggest 3 recipes I can make with these ingredients.
        For each recipe, provide:
        1. Recipe name
        2. Brief description
        3. List of ingredients with amounts (indicate which ones I have and which I need to get)
        4. Step-by-step instructions
        5. Estimated cooking time
        6. Difficulty level (Easy, Medium, or Hard)
        
        Format your response as a JSON object with the following structure:
        {{"recipes": [{{"name": "Recipe Name", "description": "Brief description", "ingredients": [{{"name": "Ingredient", "amount": "Amount", "available": true/false}}], "instructions": ["Step 1", "Step 2"], "cooking_time": minutes, "difficulty": "Easy/Medium/Hard"}}]}}
        """
        
        # Prepare API call parameters
        messages = [
            {"role": "system", "content": "You are a helpful cooking assistant that suggests recipes based on available ingredients."},
            {"role": "user", "content": prompt}
        ]
        
        # Call the API
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.7,
            max_tokens=1500,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0,
            extra_headers={
                "HTTP-Referer": "https://dishdazzle.app",  # Replace with your app's URL
                "X-Title": "DishDazzle App"
            }
        )
        
        # Extract the content from the response
        content = response.choices[0].message.content
        
        # Parse the JSON response
        # Find the JSON object in the response (it might be surrounded by markdown or other text)
        try:
            # Try to parse the entire response as JSON
            result = json.loads(content)
        except json.JSONDecodeError:
            # If that fails, try to extract the JSON object from the response
            import re
            json_match = re.search(r'\{\s*"recipes"\s*:\s*\[.+?\]\s*\}', content, re.DOTALL)
            if json_match:
                try:
                    result = json.loads(json_match.group(0))
                except json.JSONDecodeError:
                    logger.error("Failed to parse JSON from model response")
                    result = {"recipes": [], "error": "Failed to parse response"}
            else:
                logger.error("No JSON object found in model response")
                result = {"recipes": [], "error": "No valid response found"}
        
        # Cache the result
        response_cache[cache_key] = result
        
        return result
        
    except Exception as e:
        logger.error(f"Error getting recipe suggestions from {model_type}: {e}")
        return {"recipes": [], "error": str(e)}

def _get_recipe_suggestions_async(ingredients: List[str], cache_key: str, callback: Callable, model_type: str):
    """Asynchronous implementation of get_recipe_suggestions"""
    from PyQt5.QtCore import QTimer
    
    result = _get_recipe_suggestions_sync(ingredients, cache_key, model_type)
    
    # Use QTimer to safely call the callback on the main thread
    if hasattr(callback, '__self__') and hasattr(callback.__self__, 'recipe_suggestions_signal'):
        # If callback is a MainWindow method, use the signal
        callback.__self__.recipe_suggestions_signal.emit(result)
    else:
        # Otherwise use QTimer to call on main thread
        def call_on_main_thread():
            callback(result)
        
        timer = QTimer()
        timer.timeout.connect(call_on_main_thread)
        timer.setSingleShot(True)
        timer.start(0)

# [Similar updates needed for all other API functions...]

def get_ingredient_substitutions(ingredient: str, callback: Optional[Callable] = None, model_type: str = "deepseek") -> Dict[str, Any]:
    """Get substitution suggestions for an ingredient
    
    Args:
        ingredient: The ingredient to find substitutions for
        callback: Optional callback function to receive the result asynchronously
        model_type: Either "deepseek" or "llama" to specify which model to use
        
    Returns:
        Dictionary with substitution suggestions if callback is None, otherwise None
    """
    # Create a cache key
    cache_key = f"substitution:{model_type}:{ingredient.lower()}"
    
    # Check if we have a cached response
    if cache_key in response_cache:
        logger.info(f"Using cached substitution suggestions for {ingredient} from {model_type}")
        result = response_cache[cache_key]
        
        if callback:
            callback(result)
            return None
        return result
    
    # Initialize API for the specified model
    if not initialize_api(model_type):
        error_msg = f"Failed to initialize API for {model_type}"
        logger.error(error_msg)
        result = {"substitutions": [], "error": error_msg}
        
        if callback:
            callback(result)
        return result
    
    # If a callback is provided, run asynchronously
    if callback:
        thread = threading.Thread(
            target=_get_ingredient_substitutions_async,
            args=(ingredient, cache_key, callback, model_type)
        )
        thread.daemon = True
        thread.start()
        return None
    
    # Otherwise, run synchronously
    return _get_ingredient_substitutions_sync(ingredient, cache_key, model_type)

def _get_ingredient_substitutions_sync(ingredient: str, cache_key: str, model_type: str) -> Dict[str, Any]:
    """Synchronous implementation of get_ingredient_substitutions"""
    global client
    try:
        # Get config for model
        config = load_config()
        openrouter_config = config.get("api", {}).get("openrouter", {})
        
        if model_type == "deepseek":
            model = openrouter_config.get("deepseek", {}).get("model", "deepseek/deepseek-v3.1")
        else:
            model = openrouter_config.get("llama", {}).get("model", "meta-llama/llama-3-3-70b-instruct")
        
        # Prepare the prompt for the model
        prompt = f"""I don't have {ingredient} for my recipe. What are some good substitutions?
        Please provide at least 3 substitutions if possible, with the following information for each:
        1. Substitute ingredient name
        2. Substitution ratio (e.g., "1:1" or "use half as much")
        3. Brief note about flavor/texture differences
        
        Format your response as a JSON object with the following structure:
        {{"substitutions": [{{"name": "Substitute Name", "ratio": "Substitution Ratio", "notes": "Notes about differences"}}]}}
        """
        
        # Prepare API call parameters
        messages = [
            {"role": "system", "content": "You are a helpful cooking assistant that suggests ingredient substitutions."},
            {"role": "user", "content": prompt}
        ]
        
        # Call the API
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.7,
            max_tokens=800,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0,
            extra_headers={
                "HTTP-Referer": "https://dishdazzle.app",  # Replace with your app's URL
                "X-Title": "DishDazzle App"
            }
        )
        
        # Extract the content from the response
        content = response.choices[0].message.content
        
        # Parse the JSON response
        try:
            # Try to parse the entire response as JSON
            result = json.loads(content)
        except json.JSONDecodeError:
            # If that fails, try to extract the JSON object from the response
            import re
            json_match = re.search(r'\{\s*"substitutions"\s*:\s*\[.+?\]\s*\}', content, re.DOTALL)
            if json_match:
                try:
                    result = json.loads(json_match.group(0))
                except json.JSONDecodeError:
                    logger.error("Failed to parse JSON from model response")
                    result = {"substitutions": [], "error": "Failed to parse response"}
            else:
                logger.error("No JSON object found in model response")
                result = {"substitutions": [], "error": "No valid response found"}
        
        # Cache the result
        response_cache[cache_key] = result
        
        return result
        
    except Exception as e:
        logger.error(f"Error getting ingredient substitutions from {model_type}: {e}")
        return {"substitutions": [], "error": str(e)}

def _get_ingredient_substitutions_async(ingredient: str, cache_key: str, callback: Callable, model_type: str):
    """Asynchronous implementation of get_ingredient_substitutions"""
    from PyQt5.QtCore import QTimer
    
    result = _get_ingredient_substitutions_sync(ingredient, cache_key, model_type)
    
    # Use QTimer to safely call the callback on the main thread
    def call_on_main_thread():
        callback(result)
    
    timer = QTimer()
    timer.timeout.connect(call_on_main_thread)
    timer.setSingleShot(True)
    timer.start(0)

def get_cooking_assistance(query: str, recipe_context: Optional[Dict[str, Any]] = None, callback: Optional[Callable] = None, model_type: str = "deepseek") -> Dict[str, Any]:
    """Get cooking assistance from the AI chatbot
    
    Args:
        query: The user's question or request
        recipe_context: Optional context about the current recipe
        callback: Optional callback function to receive the result asynchronously
        model_type: Either "deepseek" or "llama" to specify which model to use
        
    Returns:
        Dictionary with the assistant's response if callback is None, otherwise None
    """
    # For cooking assistance, we don't cache responses as they're more conversational
    
    # Initialize API for the specified model
    if not initialize_api(model_type):
        error_msg = f"Failed to initialize API for {model_type}"
        logger.error(error_msg)
        result = {"response": error_msg, "error": error_msg}
        
        if callback:
            callback(result)
        return result
    
    # If a callback is provided, run asynchronously
    if callback:
        thread = threading.Thread(
            target=_get_cooking_assistance_async,
            args=(query, recipe_context, callback, model_type)
        )
        thread.daemon = True
        thread.start()
        return None
    
    # Otherwise, run synchronously
    return _get_cooking_assistance_sync(query, recipe_context, model_type)

def _get_cooking_assistance_sync(query: str, recipe_context: Optional[Dict[str, Any]], model_type: str) -> Dict[str, Any]:
    """Synchronous implementation of get_cooking_assistance"""
    global client
    try:
        # Get config for model
        config = load_config()
        openrouter_config = config.get("api", {}).get("openrouter", {})
        
        if model_type == "deepseek":
            model = openrouter_config.get("deepseek", {}).get("model", "deepseek/deepseek-v3.1")
        else:
            model = openrouter_config.get("llama", {}).get("model", "meta-llama/llama-3-3-70b-instruct")
        
        # Prepare the system message with recipe context if available
        system_message = "You are a helpful cooking assistant that provides guidance, tips, and answers questions about cooking."
        
        if recipe_context:
            recipe_name = recipe_context.get("name", "the recipe")
            current_step = recipe_context.get("current_step", "")
            
            system_message += f" The user is currently cooking {recipe_name}."
            
            if current_step:
                system_message += f" They are at the step: {current_step}"
        
        # Prepare API call parameters
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": query}
        ]
        
        # Call the API
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.7,
            max_tokens=800,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0,
            extra_headers={
                "HTTP-Referer": "https://dishdazzle.app",  # Replace with your app's URL
                "X-Title": "DishDazzle App"
            }
        )
        
        # Extract the content from the response
        content = response.choices[0].message.content
        
        return {"response": content}
        
    except Exception as e:
        logger.error(f"Error getting cooking assistance from {model_type}: {e}")
        return {"response": f"I'm sorry, I encountered an error: {str(e)}", "error": str(e)}

def _get_cooking_assistance_async(query: str, recipe_context: Optional[Dict[str, Any]], callback: Callable, model_type: str):
    """Asynchronous implementation of get_cooking_assistance"""
    from PyQt5.QtCore import QTimer
    
    result = _get_cooking_assistance_sync(query, recipe_context, model_type)
    
    # Use QTimer to safely call the callback on the main thread
    if hasattr(callback, '__self__') and hasattr(callback.__self__, 'assistant_response_signal'):
        # If callback is a MainWindow method, use the signal
        callback.__self__.assistant_response_signal.emit(result)
    else:
        # Otherwise use QTimer to call on main thread
        def call_on_main_thread():
            callback(result)
        
        timer = QTimer()
        timer.timeout.connect(call_on_main_thread)
        timer.setSingleShot(True)
        timer.start(0)

def get_chat_response(messages: List[Dict[str, str]], callback: Optional[Callable] = None, model_type: str = "deepseek") -> Dict[str, Any]:
    """Get a response from the AI chatbot for general conversation
    
    Args:
        messages: List of message dictionaries with 'role' and 'content' keys
        callback: Optional callback function to receive the result asynchronously
        model_type: Either "deepseek" or "llama" to specify which model to use
        
    Returns:
        Dictionary with the assistant's response if callback is None, otherwise None
    """
    # For chat, we don't cache responses as they're conversational
    
    # Initialize API for the specified model
    if not initialize_api(model_type):
        error_msg = f"Failed to initialize API for {model_type}"
        logger.error(error_msg)
        result = {"response": error_msg, "error": error_msg}
        
        if callback:
            callback(result)
        return result
    
    # If a callback is provided, run asynchronously
    if callback:
        thread = threading.Thread(
            target=_get_chat_response_async,
            args=(messages, callback, model_type)
        )
        thread.daemon = True
        thread.start()
        return None
    
    # Otherwise, run synchronously
    return _get_chat_response_sync(messages, model_type)

def _get_chat_response_sync(messages: List[Dict[str, str]], model_type: str) -> Dict[str, Any]:
    """Synchronous implementation of get_chat_response"""
    global client
    try:
        # Get config for model
        config = load_config()
        openrouter_config = config.get("api", {}).get("openrouter", {})
        
        if model_type == "deepseek":
            model = openrouter_config.get("deepseek", {}).get("model", "deepseek/deepseek-v3.1")
        else:
            model = openrouter_config.get("llama", {}).get("model", "meta-llama/llama-3-3-70b-instruct")
        
        # Ensure the first message is a system message
        if not messages or messages[0].get('role') != 'system':
            messages.insert(0, {
                "role": "system", 
                "content": "You are a helpful cooking assistant that can discuss recipes, cooking techniques, "
                           "ingredients, and other food-related topics. You can also provide general assistance "
                           "with cooking questions and offer tips for meal planning and preparation."
            })
        
        # Call the API
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.7,
            max_tokens=800,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0,
            extra_headers={
                "HTTP-Referer": "https://dishdazzle.app",  # Replace with your app's URL
                "X-Title": "DishDazzle App"
            }
        )
        
        # Extract the content from the response
        content = response.choices[0].message.content
        
        return {"response": content}
        
    except Exception as e:
        logger.error(f"Error getting chat response from {model_type}: {e}")
        return {"response": f"I'm sorry, I encountered an error: {str(e)}", "error": str(e)}

def _get_chat_response_async(messages: List[Dict[str, str]], callback: Callable, model_type: str):
    """Asynchronous implementation of get_chat_response"""
    from PyQt5.QtCore import QTimer, QObject
    import sys
    
    result = _get_chat_response_sync(messages, model_type)
    
    # Use QTimer to safely call the callback on the main thread
    if hasattr(callback, '__self__') and hasattr(callback.__self__, 'assistant_response_signal'):
        # If callback is a MainWindow method, use the signal
        callback.__self__.assistant_response_signal.emit(result)
    else:
        # Otherwise use QTimer to call on main thread
        def call_on_main_thread():
            callback(result)
        
        timer = QTimer()
        timer.timeout.connect(call_on_main_thread)
        timer.setSingleShot(True)
        timer.start(0)

def clear_cache():
    """Clear the API response cache"""
    global response_cache
    response_cache = {}
    logger.info("API response cache cleared")