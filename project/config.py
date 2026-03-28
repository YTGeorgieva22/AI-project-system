"""
Configuration and constants for the Weaviate Agents E-Commerce Application
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Weaviate Configuration
# The URL of your Weaviate Cloud instance (e.g., https://your-instance.weaviate.network)
WEAVIATE_URL = os.getenv("WEAVIATE_URL", "https://your-weaviate-cloud-url.weaviate.network")
# Your Weaviate API Key for authentication
WEAVIATE_API_KEY = os.getenv("WEAVIATE_API_KEY", "your-weaviate-api-key")

# OpenAI Configuration
# Your OpenAI API Key for vectorization and generative search
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your-openai-api-key")

# Collections Configuration
# Definition of the schema for Product and Review collections
COLLECTIONS = {
    "Product": {
        "description": "E-commerce products with descriptions and pricing",
        "properties": ["name", "description", "price", "category", "brand", "in_stock", "rating"]
    },
    "Review": {
        "description": "Customer reviews for products",
        "properties": ["text", "rating", "product_name", "reviewer_name", "helpful_count"]
    }
}

# Query Agent Configuration
# Settings for the Query Agent, including the system prompt that defines its behavior
QUERY_AGENT_CONFIG = {
    "system_prompt": """You are a helpful e-commerce assistant. You help customers find products, 
    compare options, and get information about availability and reviews. Always provide clear, 
    concise answers and offer to help with follow-up questions.""",
    "model": "gpt-4",
    "temperature": 0.7
}

# Application Settings
# Enable/disable debug mode for more verbose logging
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
# Maximum number of results to return in a search query
MAX_RESULTS = 10

