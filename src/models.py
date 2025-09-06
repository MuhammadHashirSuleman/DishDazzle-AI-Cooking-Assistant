#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
DishDazzle - Data Models
Defines data models for the application
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any


@dataclass
class Ingredient:
    """Represents a recipe ingredient"""
    name: str
    amount: str
    
    def to_dict(self) -> Dict[str, str]:
        """Convert to dictionary"""
        return {
            "name": self.name,
            "amount": self.amount
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, str]) -> 'Ingredient':
        """Create from dictionary"""
        return cls(
            name=data.get("name", ""),
            amount=data.get("amount", "")
        )


@dataclass
class Recipe:
    """Represents a recipe"""
    id: Optional[int] = None
    name: str = ""
    description: str = ""
    ingredients: List[Ingredient] = field(default_factory=list)
    instructions: List[str] = field(default_factory=list)
    cooking_time: int = 0  # in minutes
    difficulty: str = "Medium"  # Easy, Medium, Hard
    image_url: str = ""
    created_at: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "ingredients": [ingredient.to_dict() for ingredient in self.ingredients],
            "instructions": self.instructions,
            "cooking_time": self.cooking_time,
            "difficulty": self.difficulty,
            "image_url": self.image_url,
            "created_at": self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Recipe':
        """Create from dictionary"""
        ingredients = [Ingredient.from_dict(ing) for ing in data.get("ingredients", [])]
        
        return cls(
            id=data.get("id"),
            name=data.get("name", ""),
            description=data.get("description", ""),
            ingredients=ingredients,
            instructions=data.get("instructions", []),
            cooking_time=data.get("cooking_time", 0),
            difficulty=data.get("difficulty", "Medium"),
            image_url=data.get("image_url", ""),
            created_at=data.get("created_at", "")
        )


@dataclass
class GroceryItem:
    """Represents an item in the grocery list"""
    name: str
    amount: str = ""
    checked: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "name": self.name,
            "amount": self.amount,
            "checked": self.checked
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'GroceryItem':
        """Create from dictionary"""
        return cls(
            name=data.get("name", ""),
            amount=data.get("amount", ""),
            checked=data.get("checked", False)
        )


@dataclass
class PantryItem:
    """Represents an item in the pantry"""
    name: str
    amount: str = ""
    
    def to_dict(self) -> Dict[str, str]:
        """Convert to dictionary"""
        return {
            "name": self.name,
            "amount": self.amount
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, str]) -> 'PantryItem':
        """Create from dictionary"""
        return cls(
            name=data.get("name", ""),
            amount=data.get("amount", "")
        )


@dataclass
class ChatMessage:
    """Represents a chat message in the AI assistant"""
    content: str
    is_user: bool = True
    timestamp: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "content": self.content,
            "is_user": self.is_user,
            "timestamp": self.timestamp
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ChatMessage':
        """Create from dictionary"""
        return cls(
            content=data.get("content", ""),
            is_user=data.get("is_user", True),
            timestamp=data.get("timestamp", "")
        )