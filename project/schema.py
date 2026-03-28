"""
Schema setup and collection management for Weaviate
"""
from weaviate.classes.config import Configure, Property, DataType
from typing import Dict, Any


def create_product_collection(client) -> bool:
    """
    Defines the 'Product' data structure in Weaviate.
    
    Why this schema?
    We define 'Properties' like name and description with 'TEXT' data type 
    because we want the AI to be able to 'Read' and 'Understand' them.
    """
    try:
        # Avoid errors by checking if the table already exists.
        if client.collections.exists("Product"):
            print("⚠️  Product collection already exists")
            return True
        
        # We tell Weaviate to use 'text2vec-openai'. 
        # This means every product we add will automatically get a 
        # mathematical 'Vector' representing its meaning.
        client.collections.create(
            name="Product",
            description="E-commerce products with descriptions and pricing",
            properties=[
                Property(name="name", data_type=DataType.TEXT, description="Product name"),
                Property(name="description", data_type=DataType.TEXT, description="Product description"),
                Property(name="price", data_type=DataType.NUMBER, description="Product price"),
                Property(name="category", data_type=DataType.TEXT, description="Product category"),
                Property(name="brand", data_type=DataType.TEXT, description="Brand name"),
                Property(name="in_stock", data_type=DataType.BOOLEAN, description="Stock availability"),
                Property(name="rating", data_type=DataType.NUMBER, description="Average rating (0-5)"),
                Property(name="review_count", data_type=DataType.INT, description="Number of reviews"),
            ],
            vectorizer_config=Configure.Vectorizer.text2vec_openai(),
        )
        print("✅ Product collection created successfully")
        return True
    except Exception as e:
        print(f"❌ Error creating Product collection: {e}")
        return False


def create_review_collection(client) -> bool:
    """
    Defines the 'Review' collection.
    
    This is separate from Products so we can have multiple reviews 
    for a single item without making the Product object too bulky.
    """
    try:
        if client.collections.exists("Review"):
            print("⚠️  Review collection already exists")
            return True
        
        client.collections.create(
            name="Review",
            description="Customer reviews for products",
            properties=[
                Property(name="text", data_type=DataType.TEXT, description="Review text"),
                Property(name="rating", data_type=DataType.NUMBER, description="Rating (1-5)"),
                Property(name="product_name", data_type=DataType.TEXT, description="Product name"),
                Property(name="reviewer_name", data_type=DataType.TEXT, description="Reviewer name"),
                Property(name="helpful_count", data_type=DataType.INT, description="Helpful votes"),
                Property(name="verified_purchase", data_type=DataType.BOOLEAN, description="Verified purchase"),
            ],
            vectorizer_config=Configure.Vectorizer.text2vec_openai(),
        )
        print("✅ Review collection created successfully")
        return True
    except Exception as e:
        print(f"❌ Error creating Review collection: {e}")
        return False


def setup_collections(client) -> bool:
    """
    Orchestrates the creation of all necessary collections in Weaviate.
    This ensures the database schema is ready for data ingestion and querying.
    
    Args:
        client: The active Weaviate client.
        
    Returns:
        bool: True if all collections were setup correctly, False otherwise.
    """
    try:
        print("Setting up Weaviate collections...")
        # Sequentially create the product and review collections
        success = create_product_collection(client) and create_review_collection(client)
        if success:
            print("✅ All collections setup successfully")
        return success
    except Exception as e:
        print(f"❌ Error setting up collections: {e}")
        return False

