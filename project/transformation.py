from typing import Dict, Any, List, Callable
from weaviate.classes.query import Filter


class TransformationAgent:
    """
    The TransformationAgent is the 'Data Scientist' of the application.
    It is responsible for enriching raw data with new insights, tags, and summaries.
    
    Why this matters:
    In search, 'raw' data is often missing context. By using an agent to add 
    human-like tags and summaries, we make the products much easier to find 
    via natural language queries.
    """

    def __init__(self, client):
        self.client = client
        self.transformation_log = []

    def add_product_summary(self, product_name: str, summary: str) -> bool:
        """
        Adds a concise summary to a product.
        
        Why: Long descriptions are good for details, but summaries are perfect 
        for mobile displays and quick search result previews.
        """
        try:
            products = self.client.collections.get("Product")

            response = products.query.fetch_objects(
                filters=Filter.by_property("name").equal(product_name),
                limit=1
            )

            if not response.objects:
                print(f"⚠️ Product '{product_name}' not found")
                return False

            product_obj = response.objects[0]
            # We add a new 'summary' property dynamically
            product_obj.properties["summary"] = summary

            self.transformation_log.append({
                "operation": "add_summary",
                "product": product_name,
                "status": "completed"
            })

            print(f"✅ Added summary to product: {product_name}")
            return True

        except Exception as e:
            print(f"❌ Error adding summary: {e}")
            return False

    def add_product_tags(self, product_name: str, tags: List[str]) -> bool:
        """
        Attaches keywords/tags to a product.
        
        Why: Tags are great for 'faceted search' (e.g., filtering by 'Waterproof' 
        or 'Eco-friendly') which users often prefer over typing long sentences.
        """
        try:
            products = self.client.collections.get("Product")

            response = products.query.fetch_objects(
                filters=Filter.by_property("name").equal(product_name),
                limit=1
            )

            if not response.objects:
                print(f"⚠️ Product '{product_name}' not found")
                return False

            product_obj = response.objects[0]
            product_obj.properties["tags"] = tags

            self.transformation_log.append({
                "operation": "add_tags",
                "product": product_name,
                "tags_count": len(tags),
                "status": "completed"
            })

            print(f"✅ Added {len(tags)} tags to product: {product_name}")
            return True

        except Exception as e:
            print(f"❌ Error adding tags: {e}")
            return False

    def enrich_review_sentiment(self, review_id: str, sentiment_score: float) -> bool:
        """
        Analyzes and saves the sentiment of a customer review.
        
        Why: This allows the store owner to quickly identify unhappy customers 
        (low sentiment score) without reading every single review manually.
        """
        try:
            reviews = self.client.collections.get("Review")

            review_obj = reviews.query.fetch_object_by_id(review_id)

            if not review_obj:
                print(f"⚠️ Review '{review_id}' not found")
                return False

            review_obj.properties["sentiment_score"] = sentiment_score

            self.transformation_log.append({
                "operation": "add_sentiment",
                "review_id": review_id,
                "sentiment_score": sentiment_score,
                "status": "completed"
            })

            print(f"✅ Added sentiment to review: {review_id}")
            return True

        except Exception as e:
            print(f"❌ Error adding sentiment: {e}")
            return False

    def batch_enrich_products(self, enrichment_func: Callable[[Dict[str, Any]], Dict[str, Any]]) -> int:
        """
        Applies a transformation logic to the entire product catalog at once.
        
        Why: If you have 10,000 products, you don't want to update them 
        one-by-one manually. This method automates the 'mass-enrichment' process.
        """
        try:
            products = self.client.collections.get("Product")

            response = products.query.fetch_objects(limit=100)

            count = 0
            for product_obj in response.objects:
                try:
                    # enrichment_func is a custom function passed in by the developer
                    enriched = enrichment_func(product_obj.properties)
                    product_obj.properties.update(enriched)
                    count += 1
                except Exception as e:
                    print(f"⚠️ Error enriching product: {e}")

            self.transformation_log.append({
                "operation": "batch_enrich",
                "products_processed": count,
                "status": "completed"
            })

            print(f"✅ Enriched {count} products")
            return count

        except Exception as e:
            print(f"❌ Error in batch enrichment: {e}")
            return 0

    # -------------------------------
    # CATEGORY INSIGHTS
    # -------------------------------
    def add_category_insights(self, category: str, insights: Dict[str, Any]) -> bool:
        """
        Applies a set of insights or metadata to all products within a specific category.

        Args:
            category (str): The name of the category to enrich.
            insights (Dict[str, Any]): A dictionary containing the insights to add.

        Returns:
            bool: True if products were successfully updated, False otherwise.
        """
        try:
            products = self.client.collections.get("Product")

            # Find all products that belong to the specified category
            response = products.query.fetch_objects(
                filters=Filter.by_property("category").equal(category),
                limit=100
            )

            if not response.objects:
                print(f"⚠️ No products found in category: {category}")
                return False

            # Update each product in the result set with the new insights
            for product_obj in response.objects:
                product_obj.properties["category_insights"] = insights

            print(f"✅ Added insights to {len(response.objects)} products in '{category}'")
            return True

        except Exception as e:
            print(f"❌ Error adding category insights: {e}")
            return False

    # -------------------------------
    # LOGGING
    # -------------------------------
    def get_transformation_log(self) -> List[Dict[str, Any]]:
        """
        Retrieves the history of all transformations performed by this agent.

        Returns:
            List[Dict[str, Any]]: A list of log entries describing each operation.
        """
        return self.transformation_log

    def clear_log(self) -> None:
        """
        Resets the transformation log, removing all historical entries.
        """
        self.transformation_log = []
        print("✅ Transformation log cleared")