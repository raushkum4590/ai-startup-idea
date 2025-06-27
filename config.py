# Configuration file for the AI Startup Idea Generator

# OpenRouter API Configuration
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL_NAME = "mistralai/mistral-small-3.2-24b-instruct:free"

# Application Settings
APP_TITLE = "AI Startup Idea Generator & Market Validator"
APP_ICON = "🚀"
LAYOUT = "wide"

# API Settings
DEFAULT_MAX_TOKENS = 2000
VALIDATION_MAX_TOKENS = 3000
DEFAULT_TEMPERATURE = 0.7

# UI Configuration
INDUSTRIES = [
    "Technology", "Healthcare", "Education", "Finance", "E-commerce", 
    "Entertainment", "Food & Beverage", "Transportation", "Real Estate", 
    "Environment", "Fashion", "Sports", "Travel", "Other"
]

BUDGET_RANGES = [
    "Under $10K", "$10K - $50K", "$50K - $100K", 
    "$100K - $500K", "$500K+"
]

# Color Schemes
PRIMARY_COLOR = "#1f77b4"
SECONDARY_COLOR = "#2c3e50"
GRADIENT_1 = "linear-gradient(135deg, #667eea 0%, #764ba2 100%)"
GRADIENT_2 = "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)"
