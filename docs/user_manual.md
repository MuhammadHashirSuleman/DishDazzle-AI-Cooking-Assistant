# DishDazzle User Manual

## Table of Contents

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Getting Started](#getting-started)
4. [Features](#features)
   - [Recipe Management](#recipe-management)
   - [Smart Recipe Suggestions](#smart-recipe-suggestions)
   - [AI Cooking Assistant](#ai-cooking-assistant)
   - [Grocery List Management](#grocery-list-management)
   - [Step-by-Step Cooking Guide](#step-by-step-cooking-guide)
5. [Settings](#settings)
6. [Troubleshooting](#troubleshooting)
7. [FAQ](#faq)

## Introduction

DishDazzle is a modern, AI-powered desktop recipe assistant designed to transform your home cooking experience. With support for multiple AI models, beautiful Markdown formatting, and a fully responsive interface, DishDazzle helps you:

- 🔍 **Discover recipes** based on ingredients you already have
- 🤖 **Get intelligent cooking assistance** with advanced AI models
- 🛒 **Manage grocery lists** with smart pantry integration
- 👨‍🍳 **Follow step-by-step guides** with contextual help
- 🎨 **Enjoy a modern interface** that adapts to your preferences

## Installation

### System Requirements

- **Operating System**: Windows 10+, macOS 10.14+, or Linux
- **RAM**: 4GB minimum (8GB recommended for optimal performance)
- **Storage**: 500MB free disk space
- **Internet**: Required for AI features and recipe suggestions
- **Python**: 3.8+ (if running from source)

### Installation Methods

#### Method 1: Executable (Recommended)
1. Download the latest installer from the [releases page](https://github.com/yourusername/DishDazzle/releases)
2. Run the installer and follow the on-screen instructions
3. Launch DishDazzle from your applications menu or desktop shortcut

#### Method 2: From Source
1. Clone the repository: `git clone https://github.com/yourusername/DishDazzle.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Run the application: `python src/main.py`

## Getting Started

### First Launch

When you first launch DishDazzle, you'll need to configure your AI API access:

1. **Get OpenRouter API Key**: Visit [OpenRouter.ai](https://openrouter.ai/) to create an account and generate an API key
2. **Configure in Settings**: Click the **◆ Settings** button in the sidebar
3. **Enter API Key**: Add your OpenRouter API key in the Preferences dialog
4. **Choose AI Model**: Select between DeepSeek (fast, cost-effective) or Llama (advanced reasoning)
5. **Start Cooking**: Your AI cooking assistant is now ready!

### Interface Overview

DishDazzle's interface is organized into five main tabs:

1. **Recipes**: Browse, search, and manage your recipe collection.
2. **Suggestions**: Get recipe ideas based on ingredients you have.
3. **Assistant**: Chat with the AI assistant for cooking advice.
4. **Grocery & Pantry**: Manage your grocery list and pantry inventory.
5. **Cooking Guide**: Follow step-by-step instructions while cooking.

## Features

### Recipe Management

#### Browsing Recipes

- The Recipes tab displays all available recipes in a scrollable list.
- Click on a recipe to view its details, including ingredients, instructions, cooking time, and difficulty level.

#### Searching Recipes

- Use the search bar at the top of the Recipes tab to find recipes by name or ingredient.
- Type your search term and press Enter or click the search button.

#### Adding Favorites

- Click the heart icon on a recipe to add it to your favorites.
- Access your favorite recipes by clicking the "Favorites" filter button.

### Smart Recipe Suggestions

#### Getting Suggestions

1. Navigate to the Suggestions tab.
2. Enter the ingredients you have in the input field, separated by commas.
3. Click "Get Suggestions" to receive recipe ideas based on your ingredients.
4. The AI will suggest recipes from the database that match your ingredients or generate creative new recipes if no exact matches are found.

#### Ingredient Substitutions

- If you're missing an ingredient, click the "Substitutions" button next to it.
- The AI will suggest possible substitutes based on what you might have available.

### AI Cooking Assistant

#### Chatting with the Assistant

1. Go to the Assistant tab.
2. Type your cooking question in the input field at the bottom.
3. Press Enter or click the send button.
4. The AI will respond with helpful cooking advice, tips, or answers to your questions.

#### Example Questions

- "How do I know when chicken is fully cooked?"
- "What's the best way to store leftover pasta?"
- "Can I substitute olive oil with vegetable oil in this recipe?"
- "How do I fix an oversalted soup?"

### Grocery List Management

#### Adding Items Manually

1. Navigate to the Grocery & Pantry tab.
2. Enter the item name and optional amount in the input fields.
3. Click "Add Item" to add it to your grocery list.

#### Adding Items from Recipes

1. View a recipe in the Recipes tab.
2. Click "Add to Grocery List" to add all ingredients to your list.
3. The app will check your pantry and only add items you don't already have.

#### Managing Your List

- Check off items by clicking the checkbox next to them.
- Remove items by clicking the delete button.
- Clear the entire list with the "Clear List" button.
- Export your list to a text file with the "Export" button.

### Step-by-Step Cooking Guide

#### Following a Recipe

1. Go to the Cooking Guide tab.
2. Select a recipe from the dropdown menu.
3. The steps will be displayed in a list on the left.
4. Click on a step to view its details on the right.
5. Use the "Previous" and "Next" buttons to navigate between steps.

#### Getting Help with Steps

1. While viewing a step, type a question in the input field at the bottom.
2. Click "Ask" to get specific help with the current step.
3. The AI will provide contextual assistance based on the recipe and current step.

## Settings

### Theme

- Toggle between light and dark themes via the "View" menu.
- Select "Switch to Dark Theme" or "Switch to Light Theme" depending on your current setting.

### API Settings

- Access API settings via the "Settings" menu.
- You can update your OpenAI API key or change the model used for AI responses.

## Troubleshooting

### Common Issues

#### API Connection Problems

- **Issue**: Error messages about API connection failures.
- **Solution**: Check your internet connection and verify your API key is correct in the settings.

#### Slow Response Times

- **Issue**: AI responses take a long time.
- **Solution**: This could be due to high API traffic. Try again later or check if you've exceeded your API rate limits.

#### Application Crashes

- **Issue**: The application unexpectedly closes.
- **Solution**: Check the log file in the logs directory for error details. Ensure your system meets the minimum requirements.

## FAQ

### General Questions

**Q: Is my OpenAI API key secure?**  
A: Yes, your API key is stored locally in an encrypted configuration file and is never transmitted except to OpenAI's servers for API calls.

**Q: How much does it cost to use DishDazzle?**  
A: DishDazzle itself is free, but you'll need an OpenAI API key which may incur charges based on your usage. Check OpenAI's pricing for details.

**Q: Can I use DishDazzle offline?**  
A: Basic recipe browsing and grocery list management work offline, but AI features require an internet connection.

**Q: How do I add my own recipes?**  
A: Use the "Add Recipe" button in the Recipes tab to create and save your own recipes to the database.

**Q: Can I export my recipes?**  
A: Yes, you can export individual recipes or your entire collection as JSON files using the export options in the File menu.