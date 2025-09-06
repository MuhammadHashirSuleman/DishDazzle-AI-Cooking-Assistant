# 📋 Changelog

All notable changes to DishDazzle will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2024-01-06

### ✨ Added
- **Multiple AI Model Support**: Added support for DeepSeek v3.1 and Llama 3.1 70B Instruct
- **OpenRouter Integration**: Switched from direct OpenAI API to OpenRouter for better model access
- **Markdown Formatting**: Chat responses now support beautiful Markdown formatting with headers, lists, and emphasis
- **Enhanced UI Design**: Complete UI overhaul with modern, professional styling
- **Responsive Layout**: Fully responsive design that adapts to different window sizes
- **Icon System**: Replaced emojis with consistent text-based icons for cross-platform compatibility
- **Theme System**: Enhanced light and dark theme support
- **Smart Recipe Suggestions**: Improved AI-powered recipe recommendations based on available ingredients
- **Typing Indicators**: Added visual feedback when AI is processing requests
- **Enhanced Chat Interface**: Beautiful chat bubbles with proper formatting and alignment
- **Comprehensive Documentation**: Complete rewrite of all documentation with detailed guides

### 🔧 Improved
- **Performance**: Optimized UI responsiveness with proper threading and size policies
- **Error Handling**: Better error handling and user feedback throughout the application
- **Code Quality**: Cleaned up codebase with better organization and documentation
- **Configuration**: Improved settings management with better API key handling
- **Database Operations**: Enhanced database performance and reliability
- **User Experience**: Smoother interactions and better visual feedback

### 🐛 Fixed
- **Threading Issues**: Resolved Qt threading errors that caused UI freezing
- **CSS Warnings**: Removed unsupported CSS properties to eliminate console warnings
- **Button Text Visibility**: Fixed issue where button text was partially hidden
- **Layout Responsiveness**: Fixed layout issues in cooking guide and other sections
- **API Integration**: Improved API error handling and retry mechanisms
- **Memory Management**: Better resource cleanup and memory management

### 🔄 Changed
- **API Provider**: Migrated from OpenAI direct API to OpenRouter
- **Model Selection**: Updated to use newer, more capable AI models
- **UI Framework**: Enhanced PyQt5 implementation with modern design patterns
- **Project Structure**: Reorganized codebase for better maintainability
- **Documentation**: Complete documentation overhaul with comprehensive guides

### 🗑️ Removed
- **Emoji Dependencies**: Removed emoji-based icons for better compatibility
- **Legacy Code**: Cleaned up deprecated functions and unused imports
- **Unsupported CSS**: Removed CSS properties not supported by Qt

## [1.0.0] - 2023-12-01

### ✨ Added
- **Initial Release**: First stable version of DishDazzle
- **Recipe Management**: Browse, search, and save favorite recipes
- **AI Cooking Assistant**: Basic chat functionality with OpenAI GPT
- **Grocery List Management**: Create and manage grocery lists
- **Step-by-Step Cooking Guide**: Follow recipe instructions with guidance
- **Database Integration**: SQLite database for recipe storage
- **Basic UI**: Simple PyQt5 interface with tabbed navigation
- **API Integration**: OpenAI GPT API for cooking assistance
- **Configuration System**: Basic settings and API key management

### 🔧 Features
- Recipe library with search functionality
- AI-powered recipe suggestions
- Grocery list auto-generation from recipes
- Dark/light theme toggle
- Recipe favorites system
- Cooking step navigation
- Basic chat interface with AI assistant

---

## 🚀 Coming Soon

### Version 2.1 (Planned)
- 🎤 **Voice Commands**: Hands-free cooking assistance
- 📱 **Mobile Companion**: Sync with mobile devices
- 🌐 **Recipe Sharing**: Share recipes with the community
- 📊 **Nutrition Analysis**: Calorie and nutrient tracking
- 🔄 **Import/Export**: Recipe backup and sharing features

### Version 3.0 (Future)
- 🗓️ **Meal Planning**: Weekly meal planning calendar
- 🎯 **Dietary Preferences**: Personalized recommendations
- 🛒 **Smart Shopping**: Integration with grocery delivery services
- 🤖 **Advanced AI**: Even more intelligent cooking assistance
- 📈 **Analytics**: Cooking habits and preferences insights

---

## 📝 Release Notes

### How to Update

1. **Backup your data**:
   ```bash
   cp -r data/ data_backup/
   cp -r config/ config_backup/
   ```

2. **Update the application**:
   ```bash
   git pull origin main
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python src/main.py
   ```

### Migration Notes

#### Upgrading from 1.x to 2.0

- **API Configuration**: You'll need to obtain an OpenRouter API key (replaces OpenAI key)
- **Model Selection**: Choose between DeepSeek and Llama models in settings
- **UI Changes**: New responsive design may require window resizing
- **Database**: Automatic migration for existing recipes and data

### Compatibility

- **Python**: 3.8+ (3.9+ recommended)
- **Operating Systems**: Windows 10+, macOS 10.14+, Linux
- **Dependencies**: See `requirements.txt` for full list

---

## 🐛 Known Issues

### Current Version (2.0.0)

- Some complex Markdown formatting may not render perfectly in chat
- Window resizing on very small screens may cause minor layout issues
- API rate limiting may cause delays during high usage periods

### Workarounds

- For Markdown issues: Restart the chat conversation
- For layout issues: Set minimum window size to 1000x700
- For API delays: Switch between DeepSeek and Llama models

---

## 📞 Support

If you encounter any issues:

1. Check the [User Manual](docs/user_manual.md)
2. Review the [API Setup Guide](docs/api_setup_guide.md)
3. Search [existing issues](https://github.com/yourusername/DishDazzle/issues)
4. [Create a new issue](https://github.com/yourusername/DishDazzle/issues/new) if needed

---

## 🙏 Contributors

Special thanks to all contributors who made these releases possible!

- **Version 2.0**: Major UI/UX overhaul, AI model integration, responsive design
- **Version 1.0**: Initial application development, core functionality

---

*For more detailed technical information, see the [Technical Report](docs/report.md).*
