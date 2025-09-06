# 🤝 Contributing to DishDazzle

Thank you for your interest in contributing to DishDazzle! We welcome contributions from developers of all skill levels. This guide will help you get started with contributing to our AI-powered recipe assistant.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [How to Contribute](#how-to-contribute)
- [Development Guidelines](#development-guidelines)
- [Testing](#testing)
- [Documentation](#documentation)
- [Pull Request Process](#pull-request-process)
- [Community](#community)

## 📜 Code of Conduct

This project adheres to a Code of Conduct. By participating, you are expected to uphold this code:

- **Be respectful** and inclusive to all contributors
- **Be constructive** in discussions and feedback
- **Focus on the code**, not the person
- **Help others learn** and grow in the community

## 🚀 Getting Started

### Prerequisites

- **Python 3.8+** (3.9+ recommended)
- **Git** for version control
- **PyQt5** knowledge (helpful but not required)
- **Basic understanding** of AI/API integration

### Fork the Repository

1. Fork the DishDazzle repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/yourusername/DishDazzle.git
   cd DishDazzle
   ```

## 🔧 Development Setup

### 1. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### 2. Install Dependencies

```bash
# Install project dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -r requirements-dev.txt

# Or install additional dev tools manually:
pip install pytest pytest-qt pytest-cov black flake8 isort mypy
```

### 3. Set Up Pre-commit Hooks (Optional)

```bash
pip install pre-commit
pre-commit install
```

### 4. Configure Development Environment

1. Create a test configuration:
   ```bash
   cp config/config.example.json config/config.json
   ```

2. Add your development API key to `config/config.json`

3. Run the application to verify setup:
   ```bash
   python src/main.py
   ```

## 💡 How to Contribute

### 🐛 Reporting Bugs

When reporting bugs, please include:

- **Clear description** of the issue
- **Steps to reproduce** the problem
- **Expected vs actual** behavior
- **System information** (OS, Python version, etc.)
- **Screenshots or logs** if applicable

Use our [Bug Report Template](.github/ISSUE_TEMPLATE/bug_report.md).

### ✨ Suggesting Features

For feature requests, please provide:

- **Clear description** of the proposed feature
- **Use case** and motivation
- **Mockups or examples** if applicable
- **Implementation ideas** (if you have any)

Use our [Feature Request Template](.github/ISSUE_TEMPLATE/feature_request.md).

### 📝 Contributing Code

We welcome contributions in these areas:

#### 🎯 Priority Areas
- **UI/UX improvements** - Better responsive design, accessibility
- **AI integration** - New model support, improved prompts
- **Database features** - Recipe import/export, search improvements
- **Performance** - Optimization, caching, responsiveness
- **Testing** - Unit tests, integration tests, UI tests

#### 🔍 Good First Issues
Look for issues labeled `good first issue` or `beginner-friendly`.

## 📏 Development Guidelines

### 🐍 Python Code Style

We follow **PEP 8** with some modifications:

```python
# Good example
def get_recipe_suggestions(
    ingredients: List[str], 
    callback: Optional[Callable] = None
) -> Dict[str, Any]:
    """Get AI-powered recipe suggestions.
    
    Args:
        ingredients: List of available ingredients
        callback: Optional callback for async handling
        
    Returns:
        Dictionary containing recipe suggestions
    """
    if not ingredients:
        logger.warning("No ingredients provided")
        return {"recipes": [], "error": "No ingredients"}
    
    # Implementation here
    return result
```

### 📁 Code Organization

```
src/
├── main.py          # Application entry point
├── ui.py           # UI components and layouts
├── api.py          # AI API integration
├── database.py     # Database operations
├── models.py       # Data models
└── utils.py        # Utility functions
```

### 🧪 Writing Tests

Write tests for new functionality:

```python
import pytest
from src.api import get_recipe_suggestions

def test_recipe_suggestions_with_valid_ingredients():
    """Test recipe suggestions with valid ingredients."""
    ingredients = ["chicken", "rice", "vegetables"]
    result = get_recipe_suggestions(ingredients)
    
    assert "recipes" in result
    assert len(result["recipes"]) > 0
    assert not result.get("error")

def test_recipe_suggestions_with_empty_ingredients():
    """Test recipe suggestions with empty ingredient list."""
    result = get_recipe_suggestions([])
    
    assert "error" in result
    assert result["recipes"] == []
```

### 🎨 UI Development Guidelines

#### PyQt5 Best Practices

```python
# Good: Use layouts for responsive design
layout = QVBoxLayout()
layout.addWidget(widget)
layout.setSpacing(10)
layout.setContentsMargins(15, 15, 15, 15)

# Good: Set size policies
widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

# Good: Use object names for styling
button.setObjectName("primaryButton")
```

#### Responsive Design

- Use **layouts** instead of fixed positioning
- Set **minimum and maximum sizes** appropriately
- Use **size policies** for proper scaling
- Test with **different window sizes**

### 🔌 API Integration Guidelines

```python
# Good: Handle errors gracefully
try:
    response = api_call()
    return process_response(response)
except APIError as e:
    logger.error(f"API error: {e}")
    return {"error": str(e)}
except Exception as e:
    logger.exception("Unexpected error in API call")
    return {"error": "Internal error occurred"}

# Good: Use threading for non-blocking calls
def async_api_call(callback):
    thread = threading.Thread(
        target=_api_call_worker,
        args=(callback,)
    )
    thread.daemon = True
    thread.start()
```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_api.py

# Run tests matching pattern
pytest -k "test_recipe"

# Run tests with verbose output
pytest -v
```

### Test Categories

1. **Unit Tests** - Test individual functions and classes
2. **Integration Tests** - Test component interactions
3. **UI Tests** - Test user interface components
4. **API Tests** - Test external API integrations

### Writing Good Tests

- **Test one thing** per test function
- **Use descriptive names** for test functions
- **Include edge cases** and error conditions
- **Mock external dependencies** (APIs, file system)
- **Keep tests fast** and independent

## 📚 Documentation

### Code Documentation

- **Docstrings** for all public functions and classes
- **Type hints** for function parameters and returns
- **Inline comments** for complex logic
- **README updates** for new features

### User Documentation

- Update **user manual** for new features
- Add **API setup instructions** if needed
- Include **screenshots** for UI changes
- Update **troubleshooting** guide

## 🔄 Pull Request Process

### Before Creating a PR

1. **Create feature branch** from `main`:
   ```bash
   git checkout -b feature/amazing-feature
   ```

2. **Make your changes** following the guidelines

3. **Add tests** for new functionality

4. **Update documentation** as needed

5. **Run tests and linting**:
   ```bash
   pytest
   black src/ tests/
   flake8 src/ tests/
   isort src/ tests/
   ```

6. **Commit your changes**:
   ```bash
   git add .
   git commit -m "feat: add amazing feature"
   ```

### Creating the PR

1. **Push to your fork**:
   ```bash
   git push origin feature/amazing-feature
   ```

2. **Create Pull Request** on GitHub

3. **Fill out the PR template** completely

4. **Link related issues** using keywords like "Fixes #123"

### PR Review Process

1. **Automated checks** must pass (tests, linting)
2. **Code review** by maintainers
3. **Address feedback** promptly and respectfully
4. **Merge** after approval

### Commit Message Format

We use conventional commits:

```
type(scope): short description

Longer description if needed.

Fixes #123
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Test additions or changes
- `chore`: Build/tooling changes

## 👥 Community

### Communication Channels

- **GitHub Issues** - Bug reports and feature requests
- **GitHub Discussions** - General questions and ideas
- **Discord** - Real-time chat (coming soon)

### Getting Help

1. **Check documentation** first
2. **Search existing issues** for similar problems
3. **Ask questions** in GitHub Discussions
4. **Be patient and respectful** when asking for help

### Recognition

Contributors will be:
- **Listed** in the README.md
- **Credited** in release notes
- **Given appropriate GitHub badges**

## 🎉 Thank You!

Every contribution makes DishDazzle better. Whether it's:

- 🐛 **Fixing a bug**
- ✨ **Adding a feature**
- 📚 **Improving documentation**
- 🧪 **Writing tests**
- 💡 **Suggesting improvements**

Your efforts are appreciated! 

---

## 📞 Questions?

If you have any questions about contributing, please:

1. Check this guide first
2. Look through existing issues and discussions
3. Create a new discussion or issue
4. Tag maintainers if urgent: @yourusername

**Happy Contributing!** 🚀
