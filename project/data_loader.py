"""
Data loading and seeding for Weaviate
"""
from typing import List, Dict, Any
from uuid import uuid4


# Sample e-commerce data
# A list of product dictionaries used to seed the Weaviate database.
# Each product contains attributes like name, description, price, category, etc.
SAMPLE_PRODUCTS = [
    {
        "name": "Wireless Bluetooth Headphones",
        "description": "High-quality wireless headphones with noise cancellation, 30-hour battery life, and comfortable fit. Perfect for music lovers and professionals.",
        "price": 149.99,
        "category": "Electronics",
        "brand": "AudioTech",
        "in_stock": True,
        "rating": 4.5,
        "review_count": 234
    },
    {
        "name": "Stainless Steel Water Bottle",
        "description": "Durable and eco-friendly water bottle, keeps drinks cold for 24 hours or hot for 12 hours. Available in multiple colors.",
        "price": 34.99,
        "category": "Sports & Outdoors",
        "brand": "HydroFlask",
        "in_stock": True,
        "rating": 4.8,
        "review_count": 512
    },
    {
        "name": "Lightweight Running Shoes",
        "description": "Professional-grade running shoes with cushioning technology, breathable mesh, and superior grip. Ideal for marathon training.",
        "price": 129.99,
        "category": "Sports & Outdoors",
        "brand": "RunPro",
        "in_stock": True,
        "rating": 4.6,
        "review_count": 348
    },
    {
        "name": "Smart Watch Pro",
        "description": "Advanced fitness tracking smartwatch with heart rate monitor, GPS, waterproof design. Compatible with iOS and Android.",
        "price": 299.99,
        "category": "Electronics",
        "brand": "TechWear",
        "in_stock": True,
        "rating": 4.4,
        "review_count": 567
    },
    {
        "name": "Organic Green Tea Set",
        "description": "Premium organic green tea collection from various regions. Includes 5 different varieties with beautiful ceramic containers.",
        "price": 49.99,
        "category": "Food & Beverages",
        "brand": "TeaLeaf",
        "in_stock": True,
        "rating": 4.9,
        "review_count": 123
    },
    {
        "name": "Portable Phone Charger",
        "description": "Fast-charging power bank with 20000mAh capacity. Charges two devices simultaneously with LED display.",
        "price": 39.99,
        "category": "Electronics",
        "brand": "PowerHub",
        "in_stock": True,
        "rating": 4.3,
        "review_count": 892
    },
]

# A list of review dictionaries used to seed the Weaviate database.
# Each review includes the text, rating, and refers back to a product by name.
SAMPLE_REVIEWS = [
    {
        "text": "Amazing headphones! The sound quality is incredible and the noise cancellation works perfectly. Very comfortable for long listening sessions.",
        "rating": 5,
        "product_name": "Wireless Bluetooth Headphones",
        "reviewer_name": "John M.",
        "helpful_count": 156,
        "verified_purchase": True
    },
    {
        "text": "Good quality but a bit pricey. They work as advertised though. Battery lasts even longer than promised.",
        "rating": 4,
        "product_name": "Wireless Bluetooth Headphones",
        "reviewer_name": "Sarah K.",
        "helpful_count": 89,
        "verified_purchase": True
    },
    {
        "text": "The water bottle keeps my drink cold all day! Love the design and it's super durable.",
        "rating": 5,
        "product_name": "Stainless Steel Water Bottle",
        "reviewer_name": "Mike D.",
        "helpful_count": 234,
        "verified_purchase": True
    },
    {
        "text": "Perfect running shoes! Very comfortable and lightweight. Great support for long distances.",
        "rating": 5,
        "product_name": "Lightweight Running Shoes",
        "reviewer_name": "Emma R.",
        "helpful_count": 178,
        "verified_purchase": True
    },
    {
        "text": "Shoes are good but they run a bit small. Recommend sizing up half a size.",
        "rating": 4,
        "product_name": "Lightweight Running Shoes",
        "reviewer_name": "David L.",
        "helpful_count": 95,
        "verified_purchase": True
    },
    {
        "text": "The smartwatch is fantastic! Tracks everything accurately and the battery lasts 5 days.",
        "rating": 5,
        "product_name": "Smart Watch Pro",
        "reviewer_name": "Alex T.",
        "helpful_count": 203,
        "verified_purchase": True
    },
    {
        "text": "Excellent tea quality! Each variety has its own unique flavor. Worth every penny.",
        "rating": 5,
        "product_name": "Organic Green Tea Set",
        "reviewer_name": "Lisa W.",
        "helpful_count": 112,
        "verified_purchase": True
    },
    {
        "text": "The power bank charges fast and holds charge well. Very reliable for travel.",
        "rating": 5,
        "product_name": "Portable Phone Charger",
        "reviewer_name": "Tom C.",
        "helpful_count": 267,
        "verified_purchase": True
    },
]


class DataLoader:
    """
    Handles the process of loading and seeding sample data into Weaviate.
    
    This class is responsible for taking the pre-defined sample datasets 
    and inserting them into their respective collections in the vector database.
    """
    
    def __init__(self, client):
        """
        Initialize the DataLoader with a Weaviate client.
        
        Args:
            client: An instance of the Weaviate client for database interaction.
        """
        self.client = client
    
    def load_products(self) -> List[str]:
        """
        Iterates through SAMPLE_PRODUCTS and inserts them into the 'Product' collection.
        
        Returns:
            List[str]: A list of generated UUIDs for the newly inserted product records.
        """
        try:
            products = self.client.collections.get("Product")
            uuids = []
            
            for product in SAMPLE_PRODUCTS:
                uuid = products.data.insert(
                    properties=product,
                    uuid=str(uuid4())
                )
                uuids.append(uuid)
                print(f"✅ Loaded product: {product['name']}")
            
            print(f"✅ Successfully loaded {len(uuids)} products")
            return uuids
        except Exception as e:
            print(f"❌ Error loading products: {e}")
            return []
    
    def load_reviews(self) -> List[str]:
        """
        Iterates through SAMPLE_REVIEWS and inserts them into the 'Review' collection.
        
        Returns:
            List[str]: A list of generated UUIDs for the newly inserted review records.
        """
        try:
            reviews = self.client.collections.get("Review")
            uuids = []
            
            for review in SAMPLE_REVIEWS:
                uuid = reviews.data.insert(
                    properties=review,
                    uuid=str(uuid4())
                )
                uuids.append(uuid)
            
            print(f"✅ Successfully loaded {len(uuids)} reviews")
            return uuids
        except Exception as e:
            print(f"❌ Error loading reviews: {e}")
            return []
    
    def load_all_data(self) -> bool:
        """
        Orchestrates the loading of both products and reviews into the database.
        
        Returns:
            bool: True if both datasets were loaded successfully, False otherwise.
        """
        print("\n📦 Loading sample data...")
        product_uuids = self.load_products()
        review_uuids = self.load_reviews()
        return len(product_uuids) > 0 and len(review_uuids) > 0

