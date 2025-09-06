"""
DishDazzle - Modern UI Module
Implements a beautiful PyQt5 GUI with sidebar navigation and professional styling
"""

import json
import logging
from typing import Dict, List, Any, Optional, Callable

from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QStackedWidget,
    QPushButton, QLabel, QLineEdit, QTextEdit, QListWidget, QListWidgetItem,
    QComboBox, QSpinBox, QCheckBox, QRadioButton, QGroupBox, QScrollArea,
    QSplitter, QFrame, QFileDialog, QMessageBox, QProgressBar, QAction,
    QToolBar, QStatusBar, QMenu, QSizePolicy, QInputDialog, QDialog,
    QDialogButtonBox, QFormLayout, QApplication, QGraphicsDropShadowEffect
)
from PyQt5.QtCore import Qt, QSize, pyqtSignal, QThread, QTimer, QDateTime, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QIcon, QPixmap, QFont, QColor, QPalette, QPainter, QLinearGradient

from models import Recipe, Ingredient, GroceryItem, PantryItem, ChatMessage
from database import (
    get_all_recipes, get_recipe_by_id, search_recipes, add_recipe, update_recipe,
    delete_recipe, add_to_favorites, remove_from_favorites, get_favorite_recipes,
    get_pantry_ingredients, update_pantry_ingredients, get_grocery_list, update_grocery_list
)
from api import (
    initialize_api, get_recipe_suggestions, get_ingredient_substitutions,
    get_cooking_assistance, clear_cache, get_chat_response
)
from utils import load_config, update_config, export_recipe_to_json, import_recipe_from_json

# Get logger
logger = logging.getLogger(__name__)


def markdown_to_html(text):
    """Convert basic Markdown formatting to HTML"""
    import re
    
    # Convert text to string if it's not already
    if not isinstance(text, str):
        text = str(text)
    
    # Escape HTML characters first
    text = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    
    # Convert headers (### -> <h3>, ## -> <h2>, # -> <h1>)
    text = re.sub(r'^### (.+)$', r'<h3 style="color: #667eea; margin: 15px 0 10px 0;">\1</h3>', text, flags=re.MULTILINE)
    text = re.sub(r'^## (.+)$', r'<h2 style="color: #667eea; margin: 20px 0 15px 0;">\1</h2>', text, flags=re.MULTILINE)
    text = re.sub(r'^# (.+)$', r'<h1 style="color: #667eea; margin: 25px 0 20px 0;">\1</h1>', text, flags=re.MULTILINE)
    
    # Convert bold text (**text** or __text__)
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong style="color: #2d3748;">\1</strong>', text)
    text = re.sub(r'__(.+?)__', r'<strong style="color: #2d3748;">\1</strong>', text)
    
    # Convert italic text (*text* or _text_)
    text = re.sub(r'\*(.+?)\*', r'<em style="color: #4a5568;">\1</em>', text)
    text = re.sub(r'_(.+?)_', r'<em style="color: #4a5568;">\1</em>', text)
    
    # Convert code blocks (```code```)
    text = re.sub(r'```([\s\S]*?)```', r'<pre style="background-color: #f7fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 12px; margin: 10px 0; overflow-x: auto;"><code>\1</code></pre>', text)
    
    # Convert inline code (`code`)
    text = re.sub(r'`(.+?)`', r'<code style="background-color: #f7fafc; border: 1px solid #e2e8f0; border-radius: 3px; padding: 2px 4px; font-family: monospace;">\1</code>', text)
    
    # Convert unordered lists (- item or * item)
    lines = text.split('\n')
    in_list = False
    result_lines = []
    
    for line in lines:
        if re.match(r'^[-*+]\s+(.+)', line):
            if not in_list:
                result_lines.append('<ul style="margin: 10px 0; padding-left: 20px;">')
                in_list = True
            item = re.sub(r'^[-*+]\s+(.+)', r'<li style="margin: 5px 0;">\1</li>', line)
            result_lines.append(item)
        else:
            if in_list:
                result_lines.append('</ul>')
                in_list = False
            result_lines.append(line)
    
    if in_list:
        result_lines.append('</ul>')
    
    text = '\n'.join(result_lines)
    
    # Convert ordered lists (1. item)
    lines = text.split('\n')
    in_ordered_list = False
    result_lines = []
    
    for line in lines:
        if re.match(r'^\d+\.\s+(.+)', line):
            if not in_ordered_list:
                result_lines.append('<ol style="margin: 10px 0; padding-left: 20px;">')
                in_ordered_list = True
            item = re.sub(r'^\d+\.\s+(.+)', r'<li style="margin: 5px 0;">\1</li>', line)
            result_lines.append(item)
        else:
            if in_ordered_list:
                result_lines.append('</ol>')
                in_ordered_list = False
            result_lines.append(line)
    
    if in_ordered_list:
        result_lines.append('</ol>')
    
    text = '\n'.join(result_lines)
    
    # Convert line breaks
    text = text.replace('\n', '<br>')
    
    return text


class ModernButton(QPushButton):
    """Custom styled button with hover effects"""
    def __init__(self, text="", icon_text="", parent=None):
        super().__init__(text, parent)
        self.icon_text = icon_text
        self.setMinimumHeight(40)
        
    def paintEvent(self, event):
        super().paintEvent(event)
        if self.icon_text:
            painter = QPainter(self)
            painter.setFont(QFont("Segoe UI Symbol", 12))
            painter.setPen(self.palette().color(QPalette.ButtonText))
            painter.drawText(10, 25, self.icon_text)


class SidebarButton(QPushButton):
    """Custom sidebar button"""
    def __init__(self, text, icon_text="", parent=None):
        super().__init__(text, parent)
        self.icon_text = icon_text
        self.setMinimumHeight(50)
        self.setCheckable(True)
        self.setObjectName("sidebarButton")
        
    def paintEvent(self, event):
        super().paintEvent(event)
        if self.icon_text:
            painter = QPainter(self)
            painter.setFont(QFont("Segoe UI Symbol", 16))
            painter.setPen(self.palette().color(QPalette.ButtonText))
            painter.drawText(20, 30, self.icon_text)


class ChatBubble(QFrame):
    """Custom chat bubble widget with markdown support"""
    def __init__(self, message, is_user=True, parent=None):
        super().__init__(parent)
        self.is_user = is_user
        self.setMaximumWidth(650)
        self.setup_ui(message)
        
    def setup_ui(self, message):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 12, 18, 12)
        
        # Message label with improved formatting
        message_label = QLabel()
        message_label.setWordWrap(True)
        message_label.setTextFormat(Qt.RichText)
        message_label.setFont(QFont("Segoe UI", 10))
        
        # Format message based on sender
        if self.is_user:
            # User messages - simple formatting
            formatted_message = message.replace('\n', '<br>')
        else:
            # AI messages - convert markdown to HTML
            formatted_message = markdown_to_html(message)
        
        message_label.setText(formatted_message)
        
        layout.addWidget(message_label)
        
        # Styling
        if self.is_user:
            self.setObjectName("userBubble")
            layout.setAlignment(Qt.AlignRight)
        else:
            self.setObjectName("assistantBubble")
            layout.setAlignment(Qt.AlignLeft)
        
        # Add shadow effect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setColor(QColor(0, 0, 0, 30))
        shadow.setOffset(0, 2)
        self.setGraphicsEffect(shadow)


class ModernCard(QFrame):
    """Modern card widget with shadow"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("modernCard")
        
        # Add shadow effect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 40))
        shadow.setOffset(0, 5)
        self.setGraphicsEffect(shadow)


class MainWindow(QMainWindow):
    """Modern main application window"""
    
    # Custom signals for thread-safe API responses
    assistant_response_signal = pyqtSignal(object)
    recipe_suggestions_signal = pyqtSignal(object)
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__()
        
        self.config = config
        self.api_initialized = False
        self.current_recipe = None
        self.current_model_type = "deepseek"
        self.current_page = 0
        
        # Enhanced color schemes
        self.light_colors = {
            'primary': '#4f46e5',
            'primary_dark': '#4338ca',
            'primary_light': '#6366f1',
            'secondary': '#ec4899',
            'secondary_dark': '#db2777',
            'accent': '#06b6d4',
            'background': '#f8fafc',
            'surface': '#ffffff',
            'surface_elevated': '#fefefe',
            'text': '#1e293b',
            'text_light': '#64748b',
            'text_muted': '#94a3b8',
            'border': '#e2e8f0',
            'border_light': '#f1f5f9',
            'success': '#10b981',
            'success_light': '#d1fae5',
            'warning': '#f59e0b',
            'warning_light': '#fef3c7',
            'error': '#ef4444',
            'error_light': '#fee2e2',
            'sidebar': '#1e293b',
            'sidebar_text': '#ffffff',
            'chat_user': '#4f46e5',
            'chat_assistant': '#f1f5f9'
        }
        
        self.dark_colors = {
            'primary': '#6366f1',
            'primary_dark': '#4f46e5',
            'primary_light': '#7c3aed',
            'secondary': '#f472b6',
            'secondary_dark': '#ec4899',
            'accent': '#22d3ee',
            'background': '#0f172a',
            'surface': '#1e293b',
            'surface_elevated': '#334155',
            'text': '#f1f5f9',
            'text_light': '#cbd5e1',
            'text_muted': '#94a3b8',
            'border': '#334155',
            'border_light': '#475569',
            'success': '#22c55e',
            'success_light': '#166534',
            'warning': '#eab308',
            'warning_light': '#713f12',
            'error': '#ef4444',
            'error_light': '#7f1d1d',
            'sidebar': '#1e293b',
            'sidebar_text': '#f1f5f9',
            'chat_user': '#6366f1',
            'chat_assistant': '#334155'
        }
        
        # Initialize UI
        self.init_ui()
        
        # Connect signals for thread-safe API responses
        self.assistant_response_signal.connect(self.handle_assistant_response)
        self.recipe_suggestions_signal.connect(self.handle_recipe_suggestions)
        
        # Initialize API and complete setup
        self.initialize_api()
        
        # Load recipes for cooking page after UI is initialized
        QTimer.singleShot(100, self.load_cooking_recipes)
    
    def init_ui(self):
        """Initialize the modern user interface"""
        # Set window properties for better responsiveness
        self.setWindowTitle("DishDazzle - AI Recipe Assistant")
        self.setMinimumSize(1000, 700)
        self.resize(1200, 800)

         # Create status bar FIRST
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
        
        # Create progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedHeight(20)
        self.status_bar.addPermanentWidget(self.progress_bar)
        
        # Create central widget and main layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        # Create sidebar
        self.create_sidebar()
        
        # Create main content area
        self.create_main_content()
        
        # Set size policies for responsive layout
        self.sidebar.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        self.content_stack.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # Apply initial theme
        self.apply_theme()
        
        logger.info("Modern UI initialized successfully")
    
    def create_sidebar(self):
        """Create the modern sidebar navigation"""
        self.sidebar = QFrame()
        self.sidebar.setMinimumWidth(220)
        self.sidebar.setMaximumWidth(280)
        self.sidebar.setObjectName("sidebar")
        
        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(0)
        
        # Header with enhanced branding
        header = QFrame()
        header.setObjectName("sidebarHeader")
        header.setFixedHeight(100)
        
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(20, 15, 20, 15)
        header_layout.setSpacing(5)
        
        # Main title with icon
        title_layout = QHBoxLayout()
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_layout.setSpacing(12)
        
        # App icon using text symbol
        app_icon = QLabel("◆")
        app_icon.setFont(QFont("Segoe UI", 28, QFont.Bold))
        app_icon.setFixedWidth(40)
        app_icon.setAlignment(Qt.AlignCenter)
        app_icon.setObjectName("appIcon")
        
        # App title
        app_title = QLabel("DishDazzle")
        app_title.setFont(QFont("Segoe UI", 20, QFont.Bold))
        app_title.setObjectName("appTitle")
        app_title.setWordWrap(False)
        
        title_layout.addWidget(app_icon)
        title_layout.addWidget(app_title)
        title_layout.addStretch()
        
        # Subtitle with icon
        subtitle_layout = QHBoxLayout()
        subtitle_layout.setContentsMargins(0, 0, 0, 0)
        subtitle_layout.setSpacing(8)
        
        subtitle_icon = QLabel("★")
        subtitle_icon.setFont(QFont("Segoe UI", 12))
        subtitle_icon.setObjectName("subtitleIcon")
        
        app_subtitle = QLabel("Your AI Cooking Companion")
        app_subtitle.setFont(QFont("Segoe UI", 11))
        app_subtitle.setObjectName("appSubtitle")
        
        subtitle_layout.addWidget(subtitle_icon)
        subtitle_layout.addWidget(app_subtitle)
        subtitle_layout.addStretch()
        
        # Version badge
        version_badge = QLabel("v2.0")
        version_badge.setFont(QFont("Segoe UI", 9, QFont.Bold))
        version_badge.setObjectName("versionBadge")
        version_badge.setFixedSize(40, 20)
        version_badge.setAlignment(Qt.AlignCenter)
        
        subtitle_layout.addWidget(version_badge)
        
        # Add title layout
        header_layout.addLayout(title_layout)
        
        # Add subtitle layout with version badge
        header_layout.addLayout(subtitle_layout)
        
        sidebar_layout.addWidget(header)
        
        # Navigation buttons
        self.nav_buttons = []
        
        # Recipe Library
        recipes_btn = SidebarButton("Recipe Library", "☰")
        recipes_btn.clicked.connect(lambda: self.switch_page(0))
        self.nav_buttons.append(recipes_btn)
        sidebar_layout.addWidget(recipes_btn)
        
        # Recipe Suggestions
        suggestions_btn = SidebarButton("Smart Suggestions", "⚡")
        suggestions_btn.clicked.connect(lambda: self.switch_page(1))
        self.nav_buttons.append(suggestions_btn)
        sidebar_layout.addWidget(suggestions_btn)
        
        # AI Assistant
        assistant_btn = SidebarButton("Cooking Assistant", "●")
        assistant_btn.clicked.connect(lambda: self.switch_page(2))
        self.nav_buttons.append(assistant_btn)
        sidebar_layout.addWidget(assistant_btn)
        
        # Grocery & Pantry
        grocery_btn = SidebarButton("Grocery & Pantry", "□")
        grocery_btn.clicked.connect(lambda: self.switch_page(3))
        self.nav_buttons.append(grocery_btn)
        sidebar_layout.addWidget(grocery_btn)
        
        # Cooking Guide
        cooking_btn = SidebarButton("Cooking Guide", "▲")
        cooking_btn.clicked.connect(lambda: self.switch_page(4))
        self.nav_buttons.append(cooking_btn)
        sidebar_layout.addWidget(cooking_btn)
        
        # Spacer
        sidebar_layout.addStretch()
        
        # Settings section
        settings_frame = QFrame()
        settings_layout = QVBoxLayout(settings_frame)
        settings_layout.setContentsMargins(10, 10, 10, 10)
        
        # Theme toggle
        self.theme_btn = ModernButton("◐ Dark Mode")
        self.theme_btn.clicked.connect(self.toggle_theme)
        self.theme_btn.setObjectName("themeButton")
        settings_layout.addWidget(self.theme_btn)
        
        # Model selection
        model_label = QLabel("AI Model:")
        model_label.setObjectName("settingsLabel")
        settings_layout.addWidget(model_label)
        
        self.model_combo = QComboBox()
        self.model_combo.addItem("DeepSeek", "deepseek")
        self.model_combo.addItem("Llama 3.3", "llama")
        self.model_combo.currentIndexChanged.connect(self.on_model_changed)
        self.model_combo.setObjectName("settingsCombo")
        settings_layout.addWidget(self.model_combo)
        
        # Settings button
        settings_btn = ModernButton("◆ Settings")
        settings_btn.clicked.connect(self.show_preferences)
        settings_btn.setObjectName("settingsButton")
        settings_layout.addWidget(settings_btn)
        
        sidebar_layout.addWidget(settings_frame)
        
        # Select first button by default
        self.nav_buttons[0].setChecked(True)
        
        self.main_layout.addWidget(self.sidebar)
    
    def create_main_content(self):
        """Create the main content area with stacked pages"""
        self.content_stack = QStackedWidget()
        self.content_stack.setObjectName("contentStack")
        
        # Create all pages
        self.create_recipe_page()
        self.create_suggestion_page()
        self.create_assistant_page()
        self.create_grocery_page()
        self.create_cooking_page()
        
        self.main_layout.addWidget(self.content_stack)
    
    def create_recipe_page(self):
        """Create the modern Recipe Library page"""
        page = QWidget()
        page.setObjectName("contentPage")
        layout = QVBoxLayout(page)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Page header with icon
        header = self.create_page_header("Recipe Library", "Discover and manage your recipe collection", "☰")
        layout.addWidget(header)
        
        # Search section
        search_card = ModernCard()
        search_layout = QVBoxLayout(search_card)
        search_layout.setContentsMargins(20, 20, 20, 20)
        
        search_header = QLabel("Search Recipes")
        search_header.setFont(QFont("Segoe UI", 14, QFont.Bold))
        search_header.setObjectName("cardHeader")
        search_layout.addWidget(search_header)
        
        search_input_layout = QHBoxLayout()
        self.recipe_search_input = QLineEdit()
        self.recipe_search_input.setPlaceholderText("Search by name, ingredient, or cuisine...")
        self.recipe_search_input.returnPressed.connect(self.search_recipes)
        self.recipe_search_input.setObjectName("modernInput")
        
        search_button = ModernButton("▶ Search")
        search_button.clicked.connect(self.search_recipes)
        search_button.setObjectName("primaryButton")
        
        search_input_layout.addWidget(self.recipe_search_input)
        search_input_layout.addWidget(search_button)
        search_layout.addLayout(search_input_layout)
        
        # Quick actions
        actions_layout = QHBoxLayout()
        
        add_recipe_btn = ModernButton("+ Add Recipe")
        add_recipe_btn.clicked.connect(self.show_add_recipe_dialog)
        add_recipe_btn.setObjectName("successButton")
        
        favorites_btn = ModernButton("♥ Favorites")
        favorites_btn.clicked.connect(self.show_favorites)
        favorites_btn.setObjectName("warningButton")
        
        actions_layout.addWidget(add_recipe_btn)
        actions_layout.addWidget(favorites_btn)
        actions_layout.addStretch()
        
        search_layout.addLayout(actions_layout)
        layout.addWidget(search_card)
        
        # Content area
        content_splitter = QSplitter(Qt.Horizontal)
        
        # Recipe list
        list_card = ModernCard()
        list_layout = QVBoxLayout(list_card)
        list_layout.setContentsMargins(20, 20, 20, 20)
        
        list_header = QLabel("Your Recipes")
        list_header.setFont(QFont("Segoe UI", 14, QFont.Bold))
        list_header.setObjectName("cardHeader")
        list_layout.addWidget(list_header)
        
        self.recipe_list = QListWidget()
        self.recipe_list.itemClicked.connect(self.show_recipe_details)
        self.recipe_list.setObjectName("modernList")
        list_layout.addWidget(self.recipe_list)
        
        content_splitter.addWidget(list_card)
        
        # Recipe details
        details_card = ModernCard()
        details_layout = QVBoxLayout(details_card)
        details_layout.setContentsMargins(20, 20, 20, 20)
        
        self.recipe_title = QLabel("Select a recipe to view details")
        self.recipe_title.setAlignment(Qt.AlignCenter)
        self.recipe_title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        self.recipe_title.setObjectName("recipeTitle")
        details_layout.addWidget(self.recipe_title)
        
        # Scrollable details area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setObjectName("detailsScroll")
        
        details_widget = QWidget()
        self.recipe_details_layout = QVBoxLayout(details_widget)
        
        # Recipe info
        self.recipe_info = QLabel("")
        self.recipe_info.setObjectName("recipeInfo")
        self.recipe_details_layout.addWidget(self.recipe_info)
        
        # Ingredients section
        ingredients_frame = QFrame()
        ingredients_frame.setObjectName("sectionFrame")
        ingredients_layout = QVBoxLayout(ingredients_frame)
        
        ingredients_title = QLabel("Ingredients")
        ingredients_title.setFont(QFont("Segoe UI", 14, QFont.Bold))
        ingredients_title.setObjectName("sectionTitle")
        ingredients_layout.addWidget(ingredients_title)
        
        self.recipe_ingredients = QLabel("")
        self.recipe_ingredients.setWordWrap(True)
        self.recipe_ingredients.setObjectName("sectionContent")
        ingredients_layout.addWidget(self.recipe_ingredients)
        
        self.recipe_details_layout.addWidget(ingredients_frame)
        
        # Instructions section
        instructions_frame = QFrame()
        instructions_frame.setObjectName("sectionFrame")
        instructions_layout = QVBoxLayout(instructions_frame)
        
        instructions_title = QLabel("Instructions")
        instructions_title.setFont(QFont("Segoe UI", 14, QFont.Bold))
        instructions_title.setObjectName("sectionTitle")
        instructions_layout.addWidget(instructions_title)
        
        self.recipe_instructions = QLabel("")
        self.recipe_instructions.setWordWrap(True)
        self.recipe_instructions.setObjectName("sectionContent")
        instructions_layout.addWidget(self.recipe_instructions)
        
        self.recipe_details_layout.addWidget(instructions_frame)
        
        # Action buttons
        buttons_layout = QHBoxLayout()
        
        self.favorite_button = ModernButton("♥ Add to Favorites")
        self.favorite_button.clicked.connect(self.toggle_favorite)
        self.favorite_button.setObjectName("warningButton")
        
        cook_button = ModernButton("▲ Start Cooking")
        cook_button.clicked.connect(self.start_cooking)
        cook_button.setObjectName("primaryButton")
        
        grocery_button = ModernButton("+ Add to Grocery List")
        grocery_button.clicked.connect(self.add_to_grocery_list)
        grocery_button.setObjectName("successButton")
        
        buttons_layout.addWidget(self.favorite_button)
        buttons_layout.addWidget(cook_button)
        buttons_layout.addWidget(grocery_button)
        buttons_layout.addStretch()
        
        self.recipe_details_layout.addLayout(buttons_layout)
        self.recipe_details_layout.addStretch()
        
        scroll_area.setWidget(details_widget)
        details_layout.addWidget(scroll_area)
        
        content_splitter.addWidget(details_card)
        content_splitter.setSizes([350, 650])
        content_splitter.setStretchFactor(0, 0)
        content_splitter.setStretchFactor(1, 1)
        
        layout.addWidget(content_splitter)
        self.content_stack.addWidget(page)
        
        # Load recipes
        self.load_recipes()
    
    def create_suggestion_page(self):
        """Create the modern Smart Suggestions page"""
        page = QWidget()
        page.setObjectName("contentPage")
        layout = QVBoxLayout(page)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Page header with icon
        header = self.create_page_header("Smart Recipe Suggestions", "Get AI-powered recipe recommendations based on your ingredients", "⚡")
        layout.addWidget(header)
        
        # Ingredients input card
        input_card = ModernCard()
        input_layout = QVBoxLayout(input_card)
        input_layout.setContentsMargins(20, 20, 20, 20)
        
        input_header = QLabel("Available Ingredients")
        input_header.setFont(QFont("Segoe UI", 14, QFont.Bold))
        input_header.setObjectName("cardHeader")
        input_layout.addWidget(input_header)
        
        # Ingredient input
        ingredient_input_layout = QHBoxLayout()
        self.ingredient_input = QLineEdit()
        self.ingredient_input.setPlaceholderText("Enter an ingredient (e.g., chicken, tomatoes, rice...)")
        self.ingredient_input.setObjectName("modernInput")
        
        add_ingredient_btn = ModernButton("+ Add")
        add_ingredient_btn.clicked.connect(self.add_ingredient)
        add_ingredient_btn.setObjectName("primaryButton")
        
        ingredient_input_layout.addWidget(self.ingredient_input)
        ingredient_input_layout.addWidget(add_ingredient_btn)
        input_layout.addLayout(ingredient_input_layout)
        
        # Ingredients list
        self.ingredients_list = QListWidget()
        self.ingredients_list.setMaximumHeight(150)
        self.ingredients_list.setObjectName("modernList")
        input_layout.addWidget(self.ingredients_list)
        
        # Ingredient actions
        ingredient_actions = QHBoxLayout()
        
        remove_ingredient_btn = ModernButton("- Remove Selected")
        remove_ingredient_btn.clicked.connect(self.remove_ingredient)
        remove_ingredient_btn.setObjectName("errorButton")
        
        clear_ingredients_btn = ModernButton("× Clear All")
        clear_ingredients_btn.clicked.connect(self.clear_ingredients)
        clear_ingredients_btn.setObjectName("errorButton")
        
        ingredient_actions.addWidget(remove_ingredient_btn)
        ingredient_actions.addWidget(clear_ingredients_btn)
        ingredient_actions.addStretch()
        
        input_layout.addLayout(ingredient_actions)
        
        # Get suggestions button
        get_suggestions_btn = ModernButton("⚡ Get Recipe Suggestions")
        get_suggestions_btn.clicked.connect(self.get_recipe_suggestions)
        get_suggestions_btn.setObjectName("primaryButton")
        get_suggestions_btn.setMinimumHeight(50)
        input_layout.addWidget(get_suggestions_btn)
        
        layout.addWidget(input_card)
        
        # Progress bar
        self.suggestion_progress = QProgressBar()
        self.suggestion_progress.setRange(0, 0)
        self.suggestion_progress.setVisible(False)
        self.suggestion_progress.setObjectName("modernProgress")
        layout.addWidget(self.suggestion_progress)
        
        # Results card
        results_card = ModernCard()
        results_layout = QVBoxLayout(results_card)
        results_layout.setContentsMargins(20, 20, 20, 20)
        
        results_header = QLabel("Recipe Suggestions")
        results_header.setFont(QFont("Segoe UI", 14, QFont.Bold))
        results_header.setObjectName("cardHeader")
        results_layout.addWidget(results_header)
        
        self.suggestions_text = QTextEdit()
        self.suggestions_text.setReadOnly(True)
        self.suggestions_text.setObjectName("modernTextEdit")
        results_layout.addWidget(self.suggestions_text)
        
        layout.addWidget(results_card)
        self.content_stack.addWidget(page)
    
    def create_assistant_page(self):
        """Create the modern AI Assistant page with beautiful chat interface"""
        page = QWidget()
        page.setObjectName("contentPage")
        layout = QVBoxLayout(page)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Page header with icon
        header = self.create_page_header("AI Cooking Assistant", "Your personal cooking companion powered by AI", "●")
        layout.addWidget(header)
        
        # Chat container
        chat_card = ModernCard()
        chat_layout = QVBoxLayout(chat_card)
        chat_layout.setContentsMargins(0, 0, 0, 0)
        
        # Chat header
        chat_header = QFrame()
        chat_header.setObjectName("chatHeader")
        chat_header.setFixedHeight(60)
        
        header_layout = QHBoxLayout(chat_header)
        header_layout.setContentsMargins(20, 15, 20, 15)
        
        chat_title = QLabel("● Cooking Assistant")
        chat_title.setFont(QFont("Segoe UI", 14, QFont.Bold))
        chat_title.setObjectName("chatTitle")
        
        status_label = QLabel("○ Online")
        status_label.setObjectName("statusOnline")
        
        header_layout.addWidget(chat_title)
        header_layout.addStretch()
        header_layout.addWidget(status_label)
        
        chat_layout.addWidget(chat_header)
        
        # Chat messages area
        self.chat_scroll = QScrollArea()
        self.chat_scroll.setWidgetResizable(True)
        self.chat_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.chat_scroll.setObjectName("chatScroll")
        
        self.chat_widget = QWidget()
        self.chat_messages_layout = QVBoxLayout(self.chat_widget)
        self.chat_messages_layout.setContentsMargins(20, 20, 20, 20)
        self.chat_messages_layout.setSpacing(15)
        self.chat_messages_layout.addStretch()
        
        self.chat_scroll.setWidget(self.chat_widget)
        chat_layout.addWidget(self.chat_scroll)
        
        # Message input area
        input_frame = QFrame()
        input_frame.setObjectName("chatInput")
        input_frame.setFixedHeight(100)
        
        input_layout = QHBoxLayout(input_frame)
        input_layout.setContentsMargins(20, 15, 20, 15)
        
        # Message input
        self.message_input = QTextEdit()
        self.message_input.setPlaceholderText("Ask me anything about cooking, ingredients, or recipes...")
        self.message_input.setMaximumHeight(70)
        self.message_input.setObjectName("messageInput")
        
        # Send button
        send_button = ModernButton("▶ Send")
        send_button.clicked.connect(self.send_message)
        send_button.setObjectName("primaryButton")
        send_button.setMinimumWidth(80)
        send_button.setMinimumHeight(70)
        
        input_layout.addWidget(self.message_input)
        input_layout.addWidget(send_button)
        
        chat_layout.addWidget(input_frame)
        
        # Progress indicator
        self.assistant_progress = QProgressBar()
        self.assistant_progress.setRange(0, 0)
        self.assistant_progress.setVisible(False)
        self.assistant_progress.setObjectName("modernProgress")
        chat_layout.addWidget(self.assistant_progress)
        
        layout.addWidget(chat_card)
        
        # Add welcome message
        welcome_msg = "Hello! I'm your AI cooking assistant. I can help you with recipes, cooking techniques, ingredient substitutions, and more. What would you like to know?"
        self.add_chat_bubble(welcome_msg, False)
        
        self.content_stack.addWidget(page)
    
    def create_grocery_page(self):
        """Create the modern Grocery & Pantry page"""
        page = QWidget()
        page.setObjectName("contentPage")
        layout = QVBoxLayout(page)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Page header with icon
        header = self.create_page_header("Grocery & Pantry Management", "Organize your ingredients and shopping lists", "□")
        layout.addWidget(header)
        
        # Content splitter
        content_splitter = QSplitter(Qt.Horizontal)
        
        # Pantry section
        pantry_card = ModernCard()
        pantry_layout = QVBoxLayout(pantry_card)
        pantry_layout.setContentsMargins(20, 20, 20, 20)
        
        pantry_header = QLabel("□ Your Pantry")
        pantry_header.setFont(QFont("Segoe UI", 14, QFont.Bold))
        pantry_header.setObjectName("cardHeader")
        pantry_layout.addWidget(pantry_header)
        
        # Pantry input
        pantry_input_layout = QHBoxLayout()
        
        self.pantry_item_input = QLineEdit()
        self.pantry_item_input.setPlaceholderText("Enter pantry item")
        self.pantry_item_input.setObjectName("modernInput")
        
        self.pantry_amount_input = QLineEdit()
        self.pantry_amount_input.setPlaceholderText("Amount")
        self.pantry_amount_input.setMaximumWidth(100)
        self.pantry_amount_input.setObjectName("modernInput")
        
        add_pantry_btn = ModernButton("+")
        add_pantry_btn.clicked.connect(self.add_pantry_item)
        add_pantry_btn.setObjectName("primaryButton")
        add_pantry_btn.setMaximumWidth(40)
        
        pantry_input_layout.addWidget(self.pantry_item_input)
        pantry_input_layout.addWidget(self.pantry_amount_input)
        pantry_input_layout.addWidget(add_pantry_btn)
        pantry_layout.addLayout(pantry_input_layout)
        
        # Pantry list
        self.pantry_list = QListWidget()
        self.pantry_list.setObjectName("modernList")
        pantry_layout.addWidget(self.pantry_list)
        
        # Pantry actions
        pantry_actions = QHBoxLayout()
        
        remove_pantry_btn = ModernButton("- Remove")
        remove_pantry_btn.clicked.connect(self.remove_pantry_item)
        remove_pantry_btn.setObjectName("errorButton")
        
        clear_pantry_btn = ModernButton("× Clear All")
        clear_pantry_btn.clicked.connect(self.clear_pantry)
        clear_pantry_btn.setObjectName("errorButton")
        
        pantry_actions.addWidget(remove_pantry_btn)
        pantry_actions.addWidget(clear_pantry_btn)
        pantry_layout.addLayout(pantry_actions)
        
        content_splitter.addWidget(pantry_card)
        
        # Grocery section
        grocery_card = ModernCard()
        grocery_layout = QVBoxLayout(grocery_card)
        grocery_layout.setContentsMargins(20, 20, 20, 20)
        
        grocery_header = QLabel("□ Grocery List")
        grocery_header.setFont(QFont("Segoe UI", 14, QFont.Bold))
        grocery_header.setObjectName("cardHeader")
        grocery_layout.addWidget(grocery_header)
        
        # Grocery input
        grocery_input_layout = QHBoxLayout()
        
        self.grocery_item_input = QLineEdit()
        self.grocery_item_input.setPlaceholderText("Enter grocery item")
        self.grocery_item_input.setObjectName("modernInput")
        
        self.grocery_amount_input = QLineEdit()
        self.grocery_amount_input.setPlaceholderText("Amount")
        self.grocery_amount_input.setMaximumWidth(100)
        self.grocery_amount_input.setObjectName("modernInput")
        
        add_grocery_btn = ModernButton("+")
        add_grocery_btn.clicked.connect(self.add_grocery_item)
        add_grocery_btn.setObjectName("primaryButton")
        add_grocery_btn.setMaximumWidth(40)
        
        grocery_input_layout.addWidget(self.grocery_item_input)
        grocery_input_layout.addWidget(self.grocery_amount_input)
        grocery_input_layout.addWidget(add_grocery_btn)
        grocery_layout.addLayout(grocery_input_layout)
        
        # Grocery list
        self.grocery_list = QListWidget()
        self.grocery_list.setObjectName("modernList")
        grocery_layout.addWidget(self.grocery_list)
        
        # Grocery actions
        grocery_actions = QHBoxLayout()
        
        remove_grocery_btn = ModernButton("- Remove")
        remove_grocery_btn.clicked.connect(self.remove_grocery_item)
        remove_grocery_btn.setObjectName("errorButton")
        
        clear_grocery_btn = ModernButton("× Clear All")
        clear_grocery_btn.clicked.connect(self.clear_grocery_list)
        clear_grocery_btn.setObjectName("errorButton")
        
        export_grocery_btn = ModernButton("▶ Export List")
        export_grocery_btn.clicked.connect(self.export_grocery_list)
        export_grocery_btn.setObjectName("successButton")
        
        grocery_actions.addWidget(remove_grocery_btn)
        grocery_actions.addWidget(clear_grocery_btn)
        grocery_actions.addWidget(export_grocery_btn)
        grocery_layout.addLayout(grocery_actions)
        
        content_splitter.addWidget(grocery_card)
        content_splitter.setSizes([400, 400])
        content_splitter.setStretchFactor(0, 1)
        content_splitter.setStretchFactor(1, 1)
        
        layout.addWidget(content_splitter)
        self.content_stack.addWidget(page)
        
        # Load data
        self.load_pantry()
        self.load_grocery_list()
    
    def create_cooking_page(self):
        """Create the modern Cooking Guide page"""
        page = QWidget()
        page.setObjectName("contentPage")
        layout = QVBoxLayout(page)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Page header with icon
        header = self.create_page_header("Cooking Guide", "Step-by-step cooking instructions with AI assistance", "▲")
        layout.addWidget(header)
        
        # Recipe selection card
        selection_card = ModernCard()
        selection_layout = QVBoxLayout(selection_card)
        selection_layout.setContentsMargins(20, 20, 20, 20)
        
        selection_header = QLabel("Select Recipe to Cook")
        selection_header.setFont(QFont("Segoe UI", 14, QFont.Bold))
        selection_header.setObjectName("cardHeader")
        selection_layout.addWidget(selection_header)
        
        recipe_selection_layout = QHBoxLayout()
        
        self.cooking_recipe_combo = QComboBox()
        self.cooking_recipe_combo.setObjectName("modernCombo")
        recipe_selection_layout.addWidget(self.cooking_recipe_combo)
        
        load_recipe_btn = ModernButton("▲ Start Cooking")
        load_recipe_btn.clicked.connect(self.load_cooking_recipe)
        load_recipe_btn.setObjectName("primaryButton")
        recipe_selection_layout.addWidget(load_recipe_btn)
        
        selection_layout.addLayout(recipe_selection_layout)
        layout.addWidget(selection_card)
        
        # Recipe title
        self.cooking_recipe_title = QLabel("Select a recipe to begin cooking")
        self.cooking_recipe_title.setAlignment(Qt.AlignCenter)
        self.cooking_recipe_title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        self.cooking_recipe_title.setObjectName("cookingTitle")
        layout.addWidget(self.cooking_recipe_title)
        
        # Content splitter with responsive sizing
        content_splitter = QSplitter(Qt.Horizontal)
        content_splitter.setChildrenCollapsible(False)
        
        # Steps section
        steps_card = ModernCard()
        steps_card.setMinimumWidth(300)
        steps_layout = QVBoxLayout(steps_card)
        steps_layout.setContentsMargins(15, 15, 15, 15)
        
        steps_header = QLabel("▲ Cooking Steps")
        steps_header.setFont(QFont("Segoe UI", 14, QFont.Bold))
        steps_header.setObjectName("cardHeader")
        steps_layout.addWidget(steps_header)
        
        self.cooking_steps_list = QListWidget()
        self.cooking_steps_list.itemClicked.connect(self.show_step_details)
        self.cooking_steps_list.setObjectName("modernList")
        steps_layout.addWidget(self.cooking_steps_list)
        
        # Navigation
        nav_layout = QHBoxLayout()
        
        self.prev_step_button = ModernButton("◀ Previous")
        self.prev_step_button.clicked.connect(self.previous_step)
        self.prev_step_button.setObjectName("secondaryButton")
        
        self.next_step_button = ModernButton("Next ▶")
        self.next_step_button.clicked.connect(self.next_step)
        self.next_step_button.setObjectName("primaryButton")
        
        nav_layout.addWidget(self.prev_step_button)
        nav_layout.addWidget(self.next_step_button)
        steps_layout.addLayout(nav_layout)
        
        content_splitter.addWidget(steps_card)
        
        # Details and assistant section
        details_card = ModernCard()
        details_card.setMinimumWidth(400)
        details_layout = QVBoxLayout(details_card)
        details_layout.setContentsMargins(15, 15, 15, 15)
        
        # Step details
        details_header = QLabel("● Step Details")
        details_header.setFont(QFont("Segoe UI", 14, QFont.Bold))
        details_header.setObjectName("cardHeader")
        details_layout.addWidget(details_header)
        
        # Step details with scroll area for responsiveness
        details_scroll = QScrollArea()
        details_scroll.setWidgetResizable(True)
        details_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        details_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        details_scroll.setMinimumHeight(100)
        
        self.step_details_text = QLabel("Select a step to view details")
        self.step_details_text.setWordWrap(True)
        self.step_details_text.setObjectName("stepDetails")
        self.step_details_text.setAlignment(Qt.AlignTop)
        
        details_scroll.setWidget(self.step_details_text)
        details_layout.addWidget(details_scroll)
        
        # Assistant section with improved layout
        assistant_frame = QFrame()
        assistant_frame.setObjectName("assistantFrame")
        assistant_frame.setMaximumHeight(200)
        assistant_layout = QVBoxLayout(assistant_frame)
        assistant_layout.setContentsMargins(12, 12, 12, 12)
        assistant_layout.setSpacing(8)
        
        assistant_header = QLabel("● Need Help?")
        assistant_header.setFont(QFont("Segoe UI", 12, QFont.Bold))
        assistant_header.setObjectName("assistantHeader")
        assistant_layout.addWidget(assistant_header)
        
        question_layout = QHBoxLayout()
        self.step_question_input = QLineEdit()
        self.step_question_input.setPlaceholderText("Ask about this step...")
        self.step_question_input.setObjectName("modernInput")
        
        ask_btn = ModernButton("Ask")
        ask_btn.clicked.connect(self.ask_step_question)
        ask_btn.setObjectName("primaryButton")
        ask_btn.setMinimumWidth(80)
        ask_btn.setFixedHeight(32)
        
        question_layout.addWidget(self.step_question_input)
        question_layout.addWidget(ask_btn)
        assistant_layout.addLayout(question_layout)
        
        self.step_answer_text = QTextEdit()
        self.step_answer_text.setReadOnly(True)
        self.step_answer_text.setMaximumHeight(150)
        self.step_answer_text.setObjectName("modernTextEdit")
        assistant_layout.addWidget(self.step_answer_text)
        
        details_layout.addWidget(assistant_frame)
        details_layout.addStretch()
        
        content_splitter.addWidget(details_card)
        content_splitter.setSizes([350, 500])
        content_splitter.setStretchFactor(0, 0)
        content_splitter.setStretchFactor(1, 1)
        
        layout.addWidget(content_splitter)
        self.content_stack.addWidget(page)
        
        # Cooking recipes will be loaded after UI initialization
    
    def create_page_header(self, title, subtitle, icon=""):
        """Create an enhanced page header with icon"""
        header_frame = QFrame()
        header_frame.setObjectName("pageHeader")
        header_layout = QVBoxLayout(header_frame)
        header_layout.setContentsMargins(0, 0, 0, 25)
        header_layout.setSpacing(8)
        
        # Title with icon layout
        title_layout = QHBoxLayout()
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_layout.setSpacing(15)
        
        # Icon (if provided)
        if icon:
            icon_label = QLabel(icon)
            icon_label.setFont(QFont("Segoe UI", 24, QFont.Bold))
            icon_label.setFixedSize(35, 35)
            icon_label.setAlignment(Qt.AlignCenter)
            icon_label.setObjectName("pageIcon")
            title_layout.addWidget(icon_label)
        
        # Title text
        title_label = QLabel(title)
        title_label.setFont(QFont("Segoe UI", 28, QFont.Bold))
        title_label.setObjectName("pageTitle")
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        
        # Subtitle
        subtitle_label = QLabel(subtitle)
        subtitle_label.setFont(QFont("Segoe UI", 13))
        subtitle_label.setObjectName("pageSubtitle")
        subtitle_label.setMargin(5)
        
        # Decorative line
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setObjectName("headerLine")
        line.setMaximumHeight(1)
        
        header_layout.addLayout(title_layout)
        header_layout.addWidget(subtitle_label)
        header_layout.addWidget(line)
        
        return header_frame
    
    def switch_page(self, page_index):
        """Switch to the specified page"""
        # Update navigation buttons
        for i, btn in enumerate(self.nav_buttons):
            btn.setChecked(i == page_index)
        
        # Switch content
        self.content_stack.setCurrentIndex(page_index)
        self.current_page = page_index
        
        # Update status
        page_names = ["Recipe Library", "Smart Suggestions", "AI Assistant", "Grocery & Pantry", "Cooking Guide"]
        if page_index < len(page_names):
            self.status_bar.showMessage(f"Viewing {page_names[page_index]}")
    
    def add_typing_indicator(self):
        """Add a typing indicator to show AI is responding"""
        typing_bubble = QFrame()
        typing_bubble.setObjectName("typingBubble")
        typing_bubble.setMaximumWidth(120)
        
        typing_layout = QHBoxLayout(typing_bubble)
        typing_layout.setContentsMargins(18, 12, 18, 12)
        
        typing_label = QLabel("● thinking...")
        typing_label.setFont(QFont("Segoe UI", 10))
        typing_label.setObjectName("typingLabel")
        typing_layout.addWidget(typing_label)
        
        # Remove stretch before adding typing indicator
        self.chat_messages_layout.takeAt(self.chat_messages_layout.count() - 1)
        
        # Add typing indicator with proper alignment
        indicator_layout = QHBoxLayout()
        indicator_layout.addWidget(typing_bubble)
        indicator_layout.addStretch()
        indicator_layout.setContentsMargins(0, 0, 50, 0)
        
        self.chat_messages_layout.addLayout(indicator_layout)
        self.chat_messages_layout.addStretch()
        
        # Store reference to remove later
        self.typing_indicator_layout = indicator_layout
        
        # Scroll to bottom
        QTimer.singleShot(100, self.scroll_to_bottom)
    
    def remove_typing_indicator(self):
        """Remove the typing indicator"""
        if hasattr(self, 'typing_indicator_layout'):
            # Remove stretch
            self.chat_messages_layout.takeAt(self.chat_messages_layout.count() - 1)
            # Remove typing indicator
            for i in range(self.typing_indicator_layout.count()):
                widget = self.typing_indicator_layout.itemAt(i).widget()
                if widget:
                    widget.deleteLater()
            self.chat_messages_layout.removeItem(self.typing_indicator_layout)
            # Add stretch back
            self.chat_messages_layout.addStretch()
            delattr(self, 'typing_indicator_layout')
    
    def add_chat_bubble(self, message, is_user=True):
        """Add a chat bubble to the conversation"""
        # Remove typing indicator if present
        if not is_user:
            self.remove_typing_indicator()
        
        bubble = ChatBubble(message, is_user)
        
        # Remove stretch before adding new bubble
        self.chat_messages_layout.takeAt(self.chat_messages_layout.count() - 1)
        
        # Add bubble with proper alignment
        if is_user:
            bubble_layout = QHBoxLayout()
            bubble_layout.addStretch()
            bubble_layout.addWidget(bubble)
            bubble_layout.setContentsMargins(50, 0, 0, 0)
        else:
            bubble_layout = QHBoxLayout()
            bubble_layout.addWidget(bubble)
            bubble_layout.addStretch()
            bubble_layout.setContentsMargins(0, 0, 50, 0)
        
        self.chat_messages_layout.addLayout(bubble_layout)
        
        # Add stretch back
        self.chat_messages_layout.addStretch()
        
        # Scroll to bottom
        QTimer.singleShot(100, self.scroll_to_bottom)
    
    def scroll_to_bottom(self):
        """Scroll chat to bottom"""
        scrollbar = self.chat_scroll.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
    
    def apply_theme(self):
        """Apply the modern theme with beautiful styling"""
        theme = self.config.get("theme", "light")
        colors = self.dark_colors if theme == "dark" else self.light_colors
        
        # Update theme button text
        self.theme_btn.setText("○ Light Mode" if theme == "dark" else "◐ Dark Mode")
        
        # Enhanced stylesheet with improved visual design
        stylesheet = f"""
        /* Main Window */
        QMainWindow {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                stop:0 {colors['background']}, 
                stop:1 {colors['border_light']});
            color: {colors['text']};
            font-family: "Segoe UI", sans-serif;
        }}
        
        /* Sidebar */
        #sidebar {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                stop:0 {colors['sidebar']}, 
                stop:1 {colors['secondary']});
            border-right: 1px solid {colors['border']};
        }}
        
        #sidebarHeader {{
            background: transparent;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }}
        
        #appIcon {{
            color: {colors['primary_light']};
        }}
        
        #appTitle {{
            color: {colors['sidebar_text']};
            font-weight: bold;
            letter-spacing: -0.5px;
        }}
        
        #subtitleIcon {{
            color: {colors['accent']};
        }}
        
        #appSubtitle {{
            color: rgba(255, 255, 255, 0.8);
            font-weight: 400;
        }}
        
        #versionBadge {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 {colors['accent']}, stop:1 {colors['primary_light']});
            color: white;
            border-radius: 9px;
            font-weight: bold;
            padding: 2px 6px;
        }}
        
        /* Sidebar Buttons */
        #sidebarButton {{
            background: transparent;
            color: {colors['sidebar_text']};
            border: none;
            text-align: left;
            padding-left: 60px;
            font-size: 14px;
            font-weight: 500;
        }}
        
        #sidebarButton:hover {{
            background: rgba(255, 255, 255, 0.1);
        }}
        
        #sidebarButton:checked {{
            background: rgba(255, 255, 255, 0.2);
            border-left: 4px solid {colors['primary']};
        }}
        
        /* Content Area */
        #contentStack {{
            background-color: {colors['background']};
        }}
        
        #contentPage {{
            background-color: {colors['background']};
        }}
        
        /* Modern Cards */
        #modernCard {{
            background-color: {colors['surface']};
            border: 1px solid {colors['border']};
            border-radius: 12px;
            margin: 2px;
        }}
        
        /* Enhanced Page Headers */
        #pageHeader {{
            background: transparent;
            margin-bottom: 10px;
        }}
        
        #pageTitle {{
            color: {colors['text']};
            font-weight: 800;
        }}
        
        #pageSubtitle {{
            color: {colors['text_light']};
            font-weight: 400;
            margin-top: 5px;
        }}
        
        #pageIcon {{
            color: {colors['primary']};
        }}
        
        #headerLine {{
            background-color: {colors['border']};
            border: none;
            height: 2px;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 {colors['primary']}, 
                stop:0.5 {colors['accent']}, 
                stop:1 {colors['secondary']});
            border-radius: 1px;
            margin: 10px 0;
        }}
        
        /* Card Headers */
        #cardHeader {{
            color: {colors['text']};
            margin-bottom: 15px;
        }}
        
        /* Modern Inputs */
        #modernInput {{
            background-color: {colors['surface']};
            border: 2px solid {colors['border']};
            border-radius: 8px;
            padding: 12px;
            font-size: 14px;
            color: {colors['text']};
        }}
        
        #modernInput:focus {{
            border-color: {colors['primary']};
            outline: none;
        }}
        
        #modernCombo {{
            background-color: {colors['surface']};
            border: 2px solid {colors['border']};
            border-radius: 8px;
            padding: 8px 12px;
            font-size: 14px;
            color: {colors['text']};
            min-height: 20px;
        }}
        
        #modernCombo:focus {{
            border-color: {colors['primary']};
        }}
        
        #modernCombo::drop-down {{
            border: none;
            width: 30px;
        }}
        
        #modernCombo::down-arrow {{
            image: none;
            border: 2px solid {colors['text_light']};
            border-top: none;
            border-right: none;
            width: 6px;
            height: 6px;
            margin-right: 8px;
            transform: rotate(-45deg);
        }}
        
        /* Modern Lists */
        #modernList {{
            background-color: {colors['surface']};
            border: 1px solid {colors['border']};
            border-radius: 8px;
            padding: 5px;
            font-size: 14px;
            color: {colors['text']};
        }}
        
        #modernList::item {{
            padding: 12px;
            border-radius: 6px;
            margin: 2px;
        }}
        
        #modernList::item:selected {{
            background-color: {colors['primary']};
            color: white;
        }}
        
        #modernList::item:hover {{
            background-color: {colors['border']};
        }}
        
        /* Modern Text Edit */
        #modernTextEdit {{
            background-color: {colors['surface']};
            border: 1px solid {colors['border']};
            border-radius: 8px;
            padding: 12px;
            font-size: 14px;
            color: {colors['text']};
        }}
        
        /* Enhanced Modern Buttons */
        QPushButton {{
            background-color: {colors['surface_elevated']};
            color: {colors['text']};
            border: 1px solid {colors['border']};
            border-radius: 10px;
            padding: 12px 24px;
            font-size: 14px;
            font-weight: 500;
            min-height: 16px;
        }}
        
        QPushButton:hover {{
            background-color: {colors['border_light']};
            border-color: {colors['primary']};
        }}
        
        QPushButton:pressed {{
            background-color: {colors['primary']};
            color: white;
        }}
        
        #primaryButton {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 {colors['primary']}, stop:1 {colors['primary_dark']});
            color: white;
            font-weight: 600;
            border: none;
        }}
        
        #primaryButton:hover {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 {colors['primary_light']}, stop:1 {colors['primary']});
        }}
        
        #primaryButton:pressed {{
            background: {colors['primary_dark']};
        }}
        
        #successButton {{
            background-color: {colors['success']};
            color: white;
        }}
        
        #successButton:hover {{
            background-color: {colors['success']};
        }}
        
        #warningButton {{
            background-color: {colors['warning']};
            color: white;
        }}
        
        #warningButton:hover {{
            background-color: {colors['warning']};
        }}
        
        #errorButton {{
            background-color: {colors['error']};
            color: white;
        }}
        
        #errorButton:hover {{
            background-color: {colors['error']};
        }}
        
        #secondaryButton {{
            background-color: transparent;
            border: 2px solid {colors['primary']};
            color: {colors['primary']};
        }}
        
        #secondaryButton:hover {{
            background-color: {colors['primary']};
            color: white;
        }}
        
        /* Settings Buttons */
        #themeButton, #settingsButton {{
            background-color: rgba(255, 255, 255, 0.1);
            color: {colors['sidebar_text']};
            border: 1px solid rgba(255, 255, 255, 0.2);
        }}
        
        #themeButton:hover, #settingsButton:hover {{
            background-color: rgba(255, 255, 255, 0.2);
        }}
        
        #settingsLabel {{
            color: rgba(255, 255, 255, 0.8);
            font-size: 12px;
            margin-bottom: 5px;
        }}
        
        #settingsCombo {{
            background-color: rgba(255, 255, 255, 0.1);
            color: {colors['sidebar_text']};
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 6px;
        }}
        
        /* Chat Interface */
        #chatHeader {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 {colors['primary']}, stop:1 {colors['primary_dark']});
            border-top-left-radius: 12px;
            border-top-right-radius: 12px;
        }}
        
        #chatTitle {{
            color: white;
        }}
        
        #statusOnline {{
            color: {colors['success']};
            font-weight: bold;
        }}
        
        #chatScroll {{
            background-color: {colors['surface']};
            border: none;
        }}
        
        #chatInput {{
            background-color: {colors['background']};
            border-top: 1px solid {colors['border']};
        }}
        
        #messageInput {{
            background-color: {colors['surface']};
            border: 2px solid {colors['border']};
            border-radius: 20px;
            padding: 15px 20px;
            font-size: 14px;
            color: {colors['text']};
        }}
        
        #messageInput:focus {{
            border-color: {colors['primary']};
        }}
        
        /* Enhanced Chat Bubbles */
        #userBubble {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 {colors['chat_user']}, stop:1 {colors['primary_dark']});
            color: white;
            border-radius: 20px 20px 5px 20px;
            border: none;
            margin: 5px 0;
        }}
        
        #assistantBubble {{
            background-color: {colors['chat_assistant']};
            color: {colors['text']};
            border-radius: 20px 20px 20px 5px;
            border: 1px solid {colors['border']};
            margin: 5px 0;
        }}
        
        #typingBubble {{
            background-color: {colors['border_light']};
            border: 1px solid {colors['border']};
            border-radius: 20px 20px 20px 5px;
            margin: 5px 0;
        }}
        
        #typingLabel {{
            color: {colors['text_muted']};
            font-style: italic;
        }}
        
        /* Recipe Details */
        #recipeTitle {{
            color: {colors['text']};
        }}
        
        #recipeInfo {{
            color: {colors['text_light']};
            margin: 10px 0;
        }}
        
        #sectionFrame {{
            background-color: {colors['background']};
            border: 1px solid {colors['border']};
            border-radius: 8px;
            margin: 10px 0;
            padding: 10px;
        }}
        
        #sectionTitle {{
            color: {colors['text']};
        }}
        
        #sectionContent {{
            color: {colors['text_light']};
        }}
        
        /* Cooking Guide */
        #cookingTitle {{
            color: {colors['text']};
            margin: 20px 0;
        }}
        
        #stepDetails {{
            color: {colors['text']};
            background-color: {colors['background']};
            border: 1px solid {colors['border']};
            border-radius: 8px;
            padding: 15px;
            margin: 10px 0;
        }}
        
        #assistantFrame {{
            background-color: {colors['background']};
            border: 2px solid {colors['primary']};
            border-radius: 12px;
            margin-top: 20px;
        }}
        
        #assistantHeader {{
            color: {colors['primary']};
        }}
        
        /* Progress Bars */
        #modernProgress {{
            background-color: {colors['border']};
            border: none;
            border-radius: 10px;
            height: 20px;
        }}
        
        #modernProgress::chunk {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 {colors['primary']}, stop:1 {colors['primary_dark']});
            border-radius: 10px;
        }}
        
        /* Scrollbars */
        QScrollBar:vertical {{
            background-color: {colors['background']};
            width: 8px;
            border-radius: 4px;
        }}
        
        QScrollBar::handle:vertical {{
            background-color: {colors['text_light']};
            border-radius: 4px;
            min-height: 20px;
        }}
        
        QScrollBar::handle:vertical:hover {{
            background-color: {colors['primary']};
        }}
        
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: 0px;
        }}
        
        /* Status Bar */
        #modernStatusBar {{
            background-color: {colors['surface']};
            color: {colors['text_light']};
            border-top: 1px solid {colors['border']};
            padding: 5px;
        }}
        
        /* Scroll Areas */
        #detailsScroll {{
            background-color: transparent;
            border: none;
        }}
        """
        
        self.setStyleSheet(stylesheet)
    
    def toggle_theme(self):
        """Toggle between light and dark themes"""
        current_theme = self.config.get("theme", "light")
        new_theme = "dark" if current_theme == "light" else "light"
        
        # Update config
        self.config["theme"] = new_theme
        update_config("theme", new_theme)
        
        # Apply the new theme
        self.apply_theme()
        
        logger.info(f"Theme changed to {new_theme}")
    
    # All the existing backend methods remain unchanged
    # [Keep all the original methods from the original code exactly as they were]
    
    def set_model_type(self, model_type):
        """Set the current AI model type"""
        self.current_model_type = model_type
        self.model_combo.setCurrentText("DeepSeek" if model_type == "deepseek" else "Llama 3.3")
        self.status_bar.showMessage(f"Using {model_type} model")
        self.initialize_api(model_type)
    
    def on_model_changed(self, index):
        """Handle model selection change"""
        model_type = self.model_combo.currentData()
        self.set_model_type(model_type)
    
    def initialize_api(self, model_type=None):
        """Initialize the OpenRouter API"""
        if model_type is None:
            model_type = self.current_model_type
            
        self.api_initialized = initialize_api(model_type)
        
        if not self.api_initialized:
            QMessageBox.warning(
                self,
                "API Initialization Failed",
                f"Failed to initialize the OpenRouter API for {model_type}. Please check your API key in the preferences."
            )
        else:
            if hasattr(self, 'status_bar') and self.status_bar:
                self.status_bar.showMessage(f"API initialized for {model_type} model")
    
    def show_preferences(self):
        """Show the preferences dialog"""
        from PyQt5.QtWidgets import QDialog, QFormLayout, QDialogButtonBox, QComboBox, QCheckBox, QLineEdit, QGroupBox, QVBoxLayout, QLabel
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Preferences")
        dialog.setMinimumWidth(450)
        
        layout = QFormLayout(dialog)
        
        theme_combo = QComboBox()
        theme_combo.addItems(["Light", "Dark"])
        current_theme = self.config.get("theme", "light")
        theme_combo.setCurrentText(current_theme.capitalize())
        layout.addRow("Theme:", theme_combo)
        
        auto_save = QCheckBox()
        auto_save.setChecked(self.config.get("auto_save", True))
        layout.addRow("Auto-save changes:", auto_save)
        
        enable_cache = QCheckBox()
        enable_cache.setChecked(self.config.get("cache", {}).get("enabled", True))
        layout.addRow("Enable API response caching:", enable_cache)
        
        api_group = QGroupBox("API Settings")
        api_layout = QVBoxLayout()
        api_group.setLayout(api_layout)
        
        api_form = QFormLayout()
        
        model_combo = QComboBox()
        model_combo.addItem("DeepSeek", "deepseek")
        model_combo.addItem("Llama 3.3", "llama")
        
        current_model_type = self.current_model_type
        if current_model_type == "deepseek":
            model_combo.setCurrentIndex(0)
        else:
            model_combo.setCurrentIndex(1)
        
        api_form.addRow("Default AI Model:", model_combo)
        api_layout.addLayout(api_form)
        
        api_info = QLabel("Note: API keys can be set in the Settings menu.")
        api_info.setWordWrap(True)
        api_layout.addWidget(api_info)
        
        layout.addRow(api_group)
        
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        layout.addRow(button_box)
        
        if dialog.exec_() == QDialog.Accepted:
            self.config["theme"] = theme_combo.currentText().lower()
            self.config["auto_save"] = auto_save.isChecked()
            
            if "cache" not in self.config:
                self.config["cache"] = {}
            self.config["cache"]["enabled"] = enable_cache.isChecked()
            
            self.current_model_type = model_combo.currentData()
            self.model_combo.setCurrentText("DeepSeek" if self.current_model_type == "deepseek" else "Llama 3.3")
            
            # Update individual config values
            update_config("theme", self.config["theme"])
            update_config("auto_save", self.config["auto_save"])
            if "cache" in self.config:
                update_config("cache", self.config["cache"])
            
            self.apply_theme()
            
            QMessageBox.information(self, "Preferences", "Preferences updated successfully.")
    
    # Keep all the original backend methods exactly as they were
    def load_recipes(self):
        """Load all recipes into the recipe list"""
        try:
            recipes = get_all_recipes()
            
            self.recipe_list.clear()
            
            for recipe in recipes:
                item = QListWidgetItem(recipe["name"])
                item.setData(Qt.UserRole, recipe["id"])
                self.recipe_list.addItem(item)
            
            self.status_bar.showMessage(f"Loaded {len(recipes)} recipes")
            
        except Exception as e:
            logger.error(f"Error loading recipes: {e}")
            QMessageBox.critical(self, "Error", f"Failed to load recipes: {str(e)}")
    
    def search_recipes(self):
        """Search recipes by name or description"""
        query = self.recipe_search_input.text().strip()
        
        if not query:
            self.load_recipes()
            return
        
        try:
            recipes = search_recipes(query)
            
            self.recipe_list.clear()
            
            for recipe in recipes:
                item = QListWidgetItem(recipe["name"])
                item.setData(Qt.UserRole, recipe["id"])
                self.recipe_list.addItem(item)
            
            self.status_bar.showMessage(f"Found {len(recipes)} recipes matching '{query}'")
            
        except Exception as e:
            logger.error(f"Error searching recipes: {e}")
            QMessageBox.critical(self, "Error", f"Failed to search recipes: {str(e)}")
    
    def show_recipe_details(self, item):
        """Show details for the selected recipe"""
        recipe_id = item.data(Qt.UserRole)
        
        try:
            recipe = get_recipe_by_id(recipe_id)
            
            if recipe:
                self.current_recipe = recipe
                
                self.recipe_title.setText(recipe["name"])
                
                difficulty_color = "green" if recipe["difficulty"] == "Easy" else "orange" if recipe["difficulty"] == "Medium" else "red"
                
                info_text = f"<b>Cooking Time:</b> {recipe['cooking_time']} minutes<br>"
                info_text += f"<b>Difficulty:</b> <span style='color: {difficulty_color};'>{recipe['difficulty']}</span><br>"
                info_text += f"<b>Description:</b> {recipe['description']}"
                
                self.recipe_info.setText(info_text)
                
                ingredients_text = "<ul>"
                for ingredient in recipe["ingredients"]:
                    ingredients_text += f"<li><b>{ingredient['name']}:</b> {ingredient['amount']}</li>"
                ingredients_text += "</ul>"
                
                self.recipe_ingredients.setText(ingredients_text)
                
                instructions_text = "<ol>"
                for instruction in recipe["instructions"]:
                    instructions_text += f"<li>{instruction}</li>"
                instructions_text += "</ol>"
                
                self.recipe_instructions.setText(instructions_text)
                
                self.update_favorite_button(recipe_id)
                
            else:
                QMessageBox.warning(self, "Recipe Not Found", "The selected recipe could not be found.")
                
        except Exception as e:
            logger.error(f"Error showing recipe details: {e}")
            QMessageBox.critical(self, "Error", f"Failed to load recipe details: {str(e)}")
    
    def update_favorite_button(self, recipe_id):
        """Update the favorite button text based on whether the recipe is a favorite"""
        try:
            favorites = get_favorite_recipes()
            is_favorite = any(recipe["id"] == recipe_id for recipe in favorites)
            
            if is_favorite:
                self.favorite_button.setText("Remove from Favorites")
            else:
                self.favorite_button.setText("Add to Favorites")
                
        except Exception as e:
            logger.error(f"Error updating favorite button: {e}")
    
    def toggle_favorite(self):
        """Toggle the favorite status of the current recipe"""
        if not hasattr(self, "current_recipe") or not self.current_recipe:
            return
        
        recipe_id = self.current_recipe["id"]
        
        try:
            favorites = get_favorite_recipes()
            is_favorite = any(recipe["id"] == recipe_id for recipe in favorites)
            
            if is_favorite:
                if remove_from_favorites(recipe_id):
                    self.favorite_button.setText("Add to Favorites")
                    self.status_bar.showMessage(f"Removed '{self.current_recipe['name']}' from favorites")
            else:
                if add_to_favorites(recipe_id):
                    self.favorite_button.setText("Remove from Favorites")
                    self.status_bar.showMessage(f"Added '{self.current_recipe['name']}' to favorites")
                
        except Exception as e:
            logger.error(f"Error toggling favorite: {e}")
            QMessageBox.critical(self, "Error", f"Failed to update favorites: {str(e)}")
    
    def show_favorites(self):
        """Show only favorite recipes in the recipe list"""
        try:
            favorites = get_favorite_recipes()
            
            self.recipe_list.clear()
            
            for recipe in favorites:
                item = QListWidgetItem(recipe["name"])
                item.setData(Qt.UserRole, recipe["id"])
                self.recipe_list.addItem(item)
            
            self.status_bar.showMessage(f"Showing {len(favorites)} favorite recipes")
            
        except Exception as e:
            logger.error(f"Error showing favorites: {e}")
            QMessageBox.critical(self, "Error", f"Failed to load favorite recipes: {str(e)}")
    
    def start_cooking(self):
        """Start cooking the current recipe"""
        if not hasattr(self, "current_recipe") or not self.current_recipe:
            QMessageBox.warning(self, "No Recipe Selected", "Please select a recipe to start cooking.")
            return
        
        self.switch_page(4)  # Cooking Guide page
        
        index = self.cooking_recipe_combo.findText(self.current_recipe["name"])
        if index >= 0:
            self.cooking_recipe_combo.setCurrentIndex(index)
            self.load_cooking_recipe()
    
    def add_to_grocery_list(self):
        """Add ingredients from the current recipe to the grocery list"""
        if not hasattr(self, "current_recipe") or not self.current_recipe:
            QMessageBox.warning(self, "No Recipe Selected", "Please select a recipe to add ingredients to the grocery list.")
            return
        
        try:
            grocery_items = get_grocery_list()
            pantry_items = get_pantry_ingredients()
            pantry_item_names = [item["name"].lower() for item in pantry_items]
            
            added_count = 0
            for ingredient in self.current_recipe["ingredients"]:
                ingredient_name = ingredient["name"]
                
                if ingredient_name.lower() in pantry_item_names:
                    continue
                
                existing_item = next((item for item in grocery_items if item["name"].lower() == ingredient_name.lower()), None)
                
                if existing_item:
                    continue
                
                grocery_items.append({
                    "name": ingredient_name,
                    "amount": ingredient["amount"],
                    "checked": False
                })
                
                added_count += 1
            
            if update_grocery_list(grocery_items):
                self.load_grocery_list()
                
                QMessageBox.information(self, "Ingredients Added", f"Added {added_count} ingredients to your grocery list.")
                
                self.switch_page(3)  # Grocery & Pantry page
                
        except Exception as e:
            logger.error(f"Error adding to grocery list: {e}")
            QMessageBox.critical(self, "Error", f"Failed to add ingredients to grocery list: {str(e)}")
    
    def add_ingredient(self):
        """Add an ingredient to the suggestions ingredients list"""
        ingredient = self.ingredient_input.text().strip()
        
        if ingredient:
            self.ingredients_list.addItem(ingredient)
            self.ingredient_input.clear()
    
    def remove_ingredient(self):
        """Remove the selected ingredient from the suggestions ingredients list"""
        selected_items = self.ingredients_list.selectedItems()
        
        for item in selected_items:
            self.ingredients_list.takeItem(self.ingredients_list.row(item))
    
    def clear_ingredients(self):
        """Clear all ingredients from the suggestions ingredients list"""
        self.ingredients_list.clear()
    
    def get_recipe_suggestions(self):
        """Get recipe suggestions based on available ingredients"""
        if not self.api_initialized:
            QMessageBox.warning(self, "API Not Initialized", "The OpenRouter API is not initialized. Please set your API key in the preferences.")
            return
        
        ingredients = [self.ingredients_list.item(i).text() for i in range(self.ingredients_list.count())]
        
        if not ingredients:
            QMessageBox.warning(self, "No Ingredients", "Please add at least one ingredient to get suggestions.")
            return
        
        self.suggestion_progress.setVisible(True)
        self.suggestions_text.clear()
        self.suggestions_text.setPlainText("Getting recipe suggestions...")
        
        get_recipe_suggestions(ingredients, self.handle_recipe_suggestions, self.current_model_type)
    
    def handle_recipe_suggestions(self, result):
        """Handle the recipe suggestions result"""
        self.suggestion_progress.setVisible(False)
        
        if "error" in result and result["error"]:
            self.suggestions_text.setPlainText(f"Error: {result['error']}")
            return
        
        recipes = result.get("recipes", [])
        
        if not recipes:
            self.suggestions_text.setPlainText("No recipe suggestions found for your ingredients.")
            return
        
        html = "<h2>Recipe Suggestions</h2>"
        
        for i, recipe in enumerate(recipes):
            html += f"<h3>{i+1}. {recipe['name']}</h3>"
            html += f"<p><b>Description:</b> {recipe.get('description', '')}</p>"
            
            html += "<p><b>Ingredients:</b></p><ul>"
            for ingredient in recipe.get('ingredients', []):
                available = ingredient.get('available', False)
                style = "color: green;" if available else "color: red;"
                html += f"<li style='{style}'><b>{ingredient['name']}:</b> {ingredient.get('amount', '')}</li>"
            html += "</ul>"
            
            html += "<p><b>Instructions:</b></p><ol>"
            for instruction in recipe.get('instructions', []):
                html += f"<li>{instruction}</li>"
            html += "</ol>"
            
            html += f"<p><b>Cooking Time:</b> {recipe.get('cooking_time', 0)} minutes</p>"
            html += f"<p><b>Difficulty:</b> {recipe.get('difficulty', 'Medium')}</p>"
            
            if i < len(recipes) - 1:
                html += "<hr>"
        
        self.suggestions_text.setHtml(html)
    
    def send_message(self):
        """Send a message to the AI cooking assistant"""
        if not self.api_initialized:
            QMessageBox.warning(self, "API Not Initialized", "The OpenRouter API is not initialized. Please set your API key in the preferences.")
            return
        
        message = self.message_input.toPlainText().strip()
        
        if not message:
            return
        
        self.add_chat_bubble(message, True)
        self.message_input.clear()
        
        # Show typing indicator and progress
        self.add_typing_indicator()
        self.assistant_progress.setVisible(True)
        
        get_chat_response([{"role": "user", "content": message}], self.handle_assistant_response, self.current_model_type)
    
    def handle_assistant_response(self, result):
        """Handle the assistant response"""
        self.assistant_progress.setVisible(False)
        
        if "error" in result and result["error"]:
            self.add_chat_bubble(f"Error: {result['error']}", False)
            return
        
        response = result.get("response", "I'm sorry, I couldn't generate a response.")
        self.add_chat_bubble(response, False)
    
    # Continue with all the remaining original backend methods...
    def add_pantry_item(self):
        """Add an item to the pantry"""
        name = self.pantry_item_input.text().strip()
        amount = self.pantry_amount_input.text().strip()
        
        if not name:
            return
        
        try:
            pantry_items = get_pantry_ingredients()
            
            existing_item = next((item for item in pantry_items if item["name"].lower() == name.lower()), None)
            
            if existing_item:
                existing_item["amount"] = amount
            else:
                pantry_items.append({"name": name, "amount": amount})
            
            if update_pantry_ingredients(pantry_items):
                self.load_pantry()
                self.pantry_item_input.clear()
                self.pantry_amount_input.clear()
                
        except Exception as e:
            logger.error(f"Error adding pantry item: {e}")
            QMessageBox.critical(self, "Error", f"Failed to add pantry item: {str(e)}")
    
    def remove_pantry_item(self):
        """Remove the selected item from the pantry"""
        selected_items = self.pantry_list.selectedItems()
        
        if not selected_items:
            return
        
        try:
            pantry_items = get_pantry_ingredients()
            
            for item in selected_items:
                item_name = item.text().split(" - ")[0]
                pantry_items = [i for i in pantry_items if i["name"].lower() != item_name.lower()]
            
            if update_pantry_ingredients(pantry_items):
                self.load_pantry()
                
        except Exception as e:
            logger.error(f"Error removing pantry item: {e}")
            QMessageBox.critical(self, "Error", f"Failed to remove pantry item: {str(e)}")
    
    def clear_pantry(self):
        """Clear all items from the pantry"""
        try:
            if update_pantry_ingredients([]):
                self.load_pantry()
                
        except Exception as e:
            logger.error(f"Error clearing pantry: {e}")
            QMessageBox.critical(self, "Error", f"Failed to clear pantry: {str(e)}")
    
    def load_pantry(self):
        """Load pantry items into the pantry list"""
        try:
            pantry_items = get_pantry_ingredients()
            
            self.pantry_list.clear()
            
            for item in pantry_items:
                display_text = item["name"]
                if item["amount"]:
                    display_text += f" - {item['amount']}"
                
                self.pantry_list.addItem(display_text)
            
        except Exception as e:
            logger.error(f"Error loading pantry: {e}")
            QMessageBox.critical(self, "Error", f"Failed to load pantry: {str(e)}")
    
    def add_grocery_item(self):
        """Add an item to the grocery list"""
        name = self.grocery_item_input.text().strip()
        amount = self.grocery_amount_input.text().strip()
        
        if not name:
            return
        
        try:
            grocery_items = get_grocery_list()
            
            existing_item = next((item for item in grocery_items if item["name"].lower() == name.lower()), None)
            
            if existing_item:
                existing_item["amount"] = amount
            else:
                grocery_items.append({"name": name, "amount": amount, "checked": False})
            
            if update_grocery_list(grocery_items):
                self.load_grocery_list()
                self.grocery_item_input.clear()
                self.grocery_amount_input.clear()
                
        except Exception as e:
            logger.error(f"Error adding grocery item: {e}")
            QMessageBox.critical(self, "Error", f"Failed to add grocery item: {str(e)}")
    
    def remove_grocery_item(self):
        """Remove the selected item from the grocery list"""
        selected_items = self.grocery_list.selectedItems()
        
        if not selected_items:
            return
        
        try:
            grocery_items = get_grocery_list()
            
            for item in selected_items:
                item_text = item.text()
                if item_text.startswith("[x] "):
                    item_text = item_text[4:]
                
                item_name = item_text.split(" - ")[0]
                grocery_items = [i for i in grocery_items if i["name"].lower() != item_name.lower()]
            
            if update_grocery_list(grocery_items):
                self.load_grocery_list()
                
        except Exception as e:
            logger.error(f"Error removing grocery item: {e}")
            QMessageBox.critical(self, "Error", f"Failed to remove grocery item: {str(e)}")
    
    def clear_grocery_list(self):
        """Clear all items from the grocery list"""
        try:
            if update_grocery_list([]):
                self.load_grocery_list()
                
        except Exception as e:
            logger.error(f"Error clearing grocery list: {e}")
            QMessageBox.critical(self, "Error", f"Failed to clear grocery list: {str(e)}")
    
    def load_grocery_list(self):
        """Load grocery items into the grocery list"""
        try:
            grocery_items = get_grocery_list()
            
            self.grocery_list.clear()
            
            for item in grocery_items:
                display_text = ""
                if item.get("checked", False):
                    display_text = "[x] "
                
                display_text += item["name"]
                if item["amount"]:
                    display_text += f" - {item['amount']}"
                
                self.grocery_list.addItem(display_text)
            
        except Exception as e:
            logger.error(f"Error loading grocery list: {e}")
            QMessageBox.critical(self, "Error", f"Failed to load grocery list: {str(e)}")
    
    def export_grocery_list(self):
        """Export the grocery list to a text file"""
        try:
            grocery_items = get_grocery_list()
            
            if not grocery_items:
                QMessageBox.warning(self, "Empty Grocery List", "Your grocery list is empty.")
                return
            
            file_path, _ = QFileDialog.getSaveFileName(self, "Export Grocery List", "grocery_list.txt", "Text Files (*.txt)")
            
            if file_path:
                with open(file_path, "w") as f:
                    f.write("DishDazzle Grocery List\n")
                    f.write("======================\n\n")
                    
                    for item in grocery_items:
                        status = "[x]" if item.get("checked", False) else "[ ]"
                        amount = f" - {item['amount']}" if item["amount"] else ""
                        f.write(f"{status} {item['name']}{amount}\n")
                
                QMessageBox.information(self, "Export Successful", "Grocery list exported successfully!")
                
        except Exception as e:
            logger.error(f"Error exporting grocery list: {e}")
            QMessageBox.critical(self, "Error", "Failed to export grocery list: {str(e)}")
    
    def load_cooking_recipes(self):
        """Load recipes into the cooking recipe combo box"""
        try:
            recipes = get_all_recipes()
            
            self.cooking_recipe_combo.clear()
            
            for recipe in recipes:
                self.cooking_recipe_combo.addItem(recipe["name"], recipe["id"])
            
        except Exception as e:
            logger.error(f"Error loading cooking recipes: {e}")
            QMessageBox.critical(self, "Error", f"Failed to load recipes: {str(e)}")
    
    def load_cooking_recipe(self):
        """Load the selected recipe for cooking"""
        recipe_id = self.cooking_recipe_combo.currentData()
        
        if not recipe_id:
            return
        
        try:
            recipe = get_recipe_by_id(recipe_id)
            
            if recipe:
                self.cooking_recipe_title.setText(recipe["name"])
                
                self.cooking_steps_list.clear()
                
                for i, instruction in enumerate(recipe["instructions"]):
                    display_text = f"Step {i+1}: {instruction[:50]}..." if len(instruction) > 50 else f"Step {i+1}: {instruction}"
                    self.cooking_steps_list.addItem(display_text)
                
                if self.cooking_steps_list.count() > 0:
                    self.cooking_steps_list.setCurrentRow(0)
                    self.show_step_details(self.cooking_steps_list.item(0))
                
                self.update_step_navigation()
                
            else:
                QMessageBox.warning(self, "Recipe Not Found", "The selected recipe could not be found.")
                
        except Exception as e:
            logger.error(f"Error loading cooking recipe: {e}")
            QMessageBox.critical(self, "Error", f"Failed to load recipe for cooking: {str(e)}")
    
    def show_step_details(self, item):
        """Show details for the selected cooking step"""
        if not item:
            return
        
        try:
            recipe_id = self.cooking_recipe_combo.currentData()
            if not recipe_id:
                return
                
            recipe = get_recipe_by_id(recipe_id)
            if not recipe:
                return
                
            step_text = item.text()
            step_index = int(step_text.split(":")[0].replace("Step ", "")) - 1
            
            if 0 <= step_index < len(recipe["instructions"]):
                instruction = recipe["instructions"][step_index]
                self.step_details_text.setText(instruction)
                
                self.update_step_navigation()
                
        except Exception as e:
            logger.error(f"Error showing step details: {e}")
            QMessageBox.critical(self, "Error", f"Failed to show step details: {str(e)}")
    
    def update_step_navigation(self):
        """Update the step navigation buttons based on current step"""
        current_row = self.cooking_steps_list.currentRow()
        total_steps = self.cooking_steps_list.count()
        
        self.prev_step_button.setEnabled(current_row > 0)
        self.next_step_button.setEnabled(current_row < total_steps - 1)
    
    def previous_step(self):
        """Navigate to the previous cooking step"""
        current_row = self.cooking_steps_list.currentRow()
        
        if current_row > 0:
            self.cooking_steps_list.setCurrentRow(current_row - 1)
            self.show_step_details(self.cooking_steps_list.currentItem())
    
    def next_step(self):
        """Navigate to the next cooking step"""
        current_row = self.cooking_steps_list.currentRow()
        total_steps = self.cooking_steps_list.count()
        
        if current_row < total_steps - 1:
            self.cooking_steps_list.setCurrentRow(current_row + 1)
            self.show_step_details(self.cooking_steps_list.currentItem())
    
    def ask_step_question(self):
        """Ask a question about the current cooking step"""
        question = self.step_question_input.text().strip()
        
        if not question:
            QMessageBox.warning(self, "Empty Question", "Please enter a question to ask.")
            return
        
        try:
            recipe_id = self.cooking_recipe_combo.currentData()
            if not recipe_id:
                QMessageBox.warning(self, "No Recipe Selected", "Please select a recipe first.")
                return
                
            recipe = get_recipe_by_id(recipe_id)
            if not recipe:
                return
                
            current_row = self.cooking_steps_list.currentRow()
            if current_row < 0 or current_row >= len(recipe["instructions"]):
                return
                
            current_step = recipe["instructions"][current_row]
            
            self.step_answer_text.setText("Getting answer...")
            QApplication.processEvents()
            
            context = {"name": recipe["name"], "current_step": current_step}
            result = get_cooking_assistance(question, context, None, self.current_model_type)
            
            if "error" in result and result["error"]:
                self.step_answer_text.setText(f"Error: {result['error']}")
            else:
                self.step_answer_text.setText(result.get("response", "No response received."))
            
            self.step_question_input.clear()
            
        except Exception as e:
            logger.error(f"Error asking cooking question: {e}")
            QMessageBox.critical(self, "Error", f"Failed to get answer: {str(e)}")
            self.step_answer_text.setText("Error getting answer. Please try again.")
    
    def show_add_recipe_dialog(self):
        """Show the dialog to add a new recipe"""
        from PyQt5.QtWidgets import QDialog, QFormLayout, QDialogButtonBox, QTextEdit, QLineEdit, QSpinBox, QComboBox
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Add New Recipe")
        dialog.setMinimumWidth(500)
        
        layout = QFormLayout(dialog)
        
        name_input = QLineEdit()
        name_input.setPlaceholderText("Enter recipe name")
        layout.addRow("Name:", name_input)
        
        description_input = QTextEdit()
        description_input.setMaximumHeight(80)
        description_input.setPlaceholderText("Enter recipe description")
        layout.addRow("Description:", description_input)
        
        cooking_time_input = QSpinBox()
        cooking_time_input.setRange(1, 500)
        cooking_time_input.setSuffix(" minutes")
        layout.addRow("Cooking Time:", cooking_time_input)
        
        difficulty_input = QComboBox()
        difficulty_input.addItems(["Easy", "Medium", "Hard"])
        layout.addRow("Difficulty:", difficulty_input)
        
        ingredients_input = QTextEdit()
        ingredients_input.setMaximumHeight(120)
        ingredients_input.setPlaceholderText("Enter ingredients (one per line)\nFormat: Name - Amount")
        layout.addRow("Ingredients:", ingredients_input)
        
        instructions_input = QTextEdit()
        instructions_input.setMaximumHeight(200)
        instructions_input.setPlaceholderText("Enter instructions (one per line)")
        layout.addRow("Instructions:", instructions_input)
        
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        layout.addRow(button_box)
        
        if dialog.exec_() == QDialog.Accepted:
            ingredients = []
            for line in ingredients_input.toPlainText().split('\n'):
                line = line.strip()
                if line:
                    if ' - ' in line:
                        name, amount = line.split(' - ', 1)
                        ingredients.append({"name": name.strip(), "amount": amount.strip()})
                    else:
                        ingredients.append({"name": line, "amount": ""})
            
            instructions = [line.strip() for line in instructions_input.toPlainText().split('\n') if line.strip()]
            
            recipe_data = {
                "name": name_input.text(),
                "description": description_input.toPlainText(),
                "cooking_time": cooking_time_input.value(),
                "difficulty": difficulty_input.currentText(),
                "ingredients": ingredients,
                "instructions": instructions
            }
            
            try:
                recipe_id = add_recipe(recipe_data)
                
                if recipe_id:
                    QMessageBox.information(self, "Recipe Added", f"Recipe '{recipe_data['name']}' added successfully!")
                    
                    self.load_recipes()
                    self.load_cooking_recipes()
                else:
                    QMessageBox.warning(self, "Add Failed", "Failed to add the recipe to the database.")
            except Exception as e:
                QMessageBox.critical(self, "Add Error", f"Error adding recipe: {str(e)}")