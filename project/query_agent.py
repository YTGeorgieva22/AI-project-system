from typing import List, Dict, Any
from weaviate.classes.query import Filter


class QueryAgent:
    """
    The QueryAgent is the 'Voice' of the application. 
    It translates human questions into database searches.
    
    Architecture Pattern: Progressive Fallback
    1. Try High-Level AI (Native Weaviate Agent)
    2. Fallback to Multi-Collection Keyword Search (BM25)
    3. Format results into human-readable text
    """
    
    def __init__(self, client):
        self.client = client
        # This prompt guides the AI on how to behave and what data it has access to.
        self.system_prompt = """You are a helpful e-commerce assistant. 
        You help customers find products, compare options, check availability and read reviews.
        You have access to two main collections:
        1. Product - contains product information like name, description, price, category, brand, stock status, and ratings
        2. Review - contains customer reviews with ratings and feedback
        """

    def ask(self, question: str) -> Dict[str, Any]:
        """
        Main entry point for any user question.
        
        Why this logic?
        It uses 'Feature Detection' to check if the Weaviate cluster supports 
        the newer Agent API. If it doesn't, it gracefully degrades to a 
        standard search so the user never sees a crash.
        """
        try:
            print(f"\n🤔 Processing question: {question}\n")

            agents = self.client.agents

            # Attempt 1: Use the Native AI Agent
            if hasattr(agents, 'query_agent'):
                result = agents.query_agent.generate(
                    question=question,
                    system_prompt=self.system_prompt
                )
                return {
                    "question": question,
                    "answer": result,
                    "success": True
                }
            # Attempt 2: Fallback if Agent API is missing
            else:
                return self._fallback_search(question)

        except AttributeError:
            return self._fallback_search(question)

        except Exception as e:
            return {
                "question": question,
                "answer": str(e),
                "success": False
            }

    def _fallback_search(self, question: str) -> Dict[str, Any]:
        """
        Performs a keyword-based search across multiple collections simultaneously.
        
        Why BM25?
        BM25 (Best Matching 25) is the industry standard for keyword search. 
        It's faster than vector search and better for specific product names or brands.
        """
        try:
            results = {
                "products": self._search_products(question),
                "reviews": self._search_reviews(question)
            }

            # Turn raw JSON data into a nice string for the user
            answer = self._format_search_results(results)

            return {
                "question": question,
                "answer": answer,
                "results": results,
                "success": True
            }

        except Exception as e:
            return {
                "question": question,
                "answer": str(e),
                "success": False
            }

    def _search_products(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Searches the 'Product' collection using keyword relevance.
        """
        try:
            products = self.client.collections.get("Product")

            # We use bm25 here to find products that exactly match the words in the query.
            response = products.query.bm25(
                query=query,
                limit=limit
            )

            return [obj.properties for obj in response.objects]

        except Exception as e:
            print(f"⚠️ Product search error: {e}")
            return []

    def _search_reviews(self, query: str, limit: int = 3) -> List[Dict[str, Any]]:
        """
        Searches the 'Review' collection. 
        Useful for queries like 'Is this product good for travel?'
        """
        try:
            reviews = self.client.collections.get("Review")

            response = reviews.query.bm25(
                query=query,
                limit=limit
            )

            return [obj.properties for obj in response.objects]

        except Exception as e:
            print(f"⚠️ Review search error: {e}")
            return []

    # -------------------------------

    # CATEGORY FILTER
    # -------------------------------
    def search_products_by_category(self, category: str) -> List[Dict[str, Any]]:
        """
        Retrieves products belonging to a specific category.

        Args:
            category (str): The name of the category to filter by.

        Returns:
            List[Dict[str, Any]]: A list of product properties matching the category.
        """
        try:
            products = self.client.collections.get("Product")

            # Fetch objects with a precise property filter
            response = products.query.fetch_objects(
                filters=Filter.by_property("category").equal(category),
                limit=10
            )

            return [obj.properties for obj in response.objects]

        except Exception as e:
            print(f"❌ Category search error: {e}")
            return []

    # -------------------------------
    # TOP RATED
    # -------------------------------
    def get_top_rated_products(self, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Retrieves the highest-rated products across the entire catalog.

        Args:
            limit (int): The maximum number of top-rated products to return.

        Returns:
            List[Dict[str, Any]]: A list of product properties sorted by rating.
        """
        try:
            products = self.client.collections.get("Product")

            # Fetch a sample of products to perform in-memory sorting
            response = products.query.fetch_objects(limit=50)

            results = [obj.properties for obj in response.objects]

            # Sort the results by rating in descending order, handling missing ratings gracefully
            results.sort(key=lambda x: x.get("rating") or 0, reverse=True)

            return results[:limit]

        except Exception as e:
            print(f"❌ Top rated error: {e}")
            return []

    # -------------------------------
    # FORMAT RESULTS
    # -------------------------------
    def _format_search_results(self, results: Dict[str, Any]) -> str:
        """
        Converts raw search results into a user-friendly string format.

        Args:
            results (Dict[str, Any]): A dictionary containing 'products' and 'reviews' lists.

        Returns:
            str: A formatted string representing the search results.
        """
        answer = ""

        # Format product information if any results were found
        if results.get("products"):
            answer += "📦 Matching Products:\n"
            for i, p in enumerate(results["products"], 1):
                answer += f"\n{i}. {p.get('name')} (${p.get('price')})"
                answer += f"\n   ⭐ {p.get('rating')} | Stock: {'Yes' if p.get('in_stock') else 'No'}\n"

        # Format review information if any results were found
        if results.get("reviews"):
            answer += "\n💬 Reviews:\n"
            for r in results["reviews"]:
                answer += f"\n⭐ {r.get('rating')} - {r.get('text')[:100]}...\n"

        # Provide a default message if no matches were found in either collection
        if not answer:
            answer = "No results found."

        return answer