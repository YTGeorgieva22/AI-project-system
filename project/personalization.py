"""
Personalization Agent - Creates user profiles and personalized recommendations
"""
from typing import Dict, Any, List
from datetime import datetime


class PersonalizationAgent:
    """
    The PersonalizationAgent is responsible for building "User Personas" and 
    generating tailored product recommendations.
    
    Why this approach?
    Instead of complex Machine Learning models that require thousands of data points, 
    this uses a 'Heuristic Scoring' system. This is ideal for startups or MVPs 
    where you need immediate results with a small amount of data.
    """
    
    def __init__(self, client):
        """
        Initializes the agent with a Weaviate client and in-memory storage for personas.
        Note: In a production app, user_profiles should be moved to a persistent 
        database like PostgreSQL or Redis.
        """
        self.client = client
        self.user_profiles = {}
        self.interactions = {}
    
    def create_user_persona(self, user_id: str, preferences: Dict[str, Any]) -> Dict[str, Any]:
        """
        Creates a new user profile with their explicit preferences.
        
        Why: Explicit preferences (like 'I love electronics') are 'strong signals' 
        that help the cold-start problem when a user first joins the platform.
        """
        self.user_profiles[user_id] = {
            "user_id": user_id,
            "preferences": preferences,
            "created_at": datetime.now().isoformat(),
            "interaction_count": 0,
            "interaction_history": []
        }
        print(f"✅ Created persona for user: {user_id}")
        print(f"   Preferences: {preferences}")
        return self.user_profiles[user_id]
    
    def record_interaction(self, user_id: str, product_name: str, interaction_type: str, details: Dict[str, Any] = None) -> bool:
        """
        Tracks what a user does on the site (clicks, purchases, etc.).
        
        Why: This 'implicit' data allows the agent to refine its recommendations 
        over time based on actual behavior rather than just what the user said they liked.
        """
        if user_id not in self.user_profiles:
            print(f"⚠️  User {user_id} not found")
            return False
        
        interaction = {
            "timestamp": datetime.now().isoformat(),
            "product_name": product_name,
            "type": interaction_type,
            "details": details or {}
        }
        
        self.user_profiles[user_id]["interaction_history"].append(interaction)
        self.user_profiles[user_id]["interaction_count"] += 1
        
        print(f"✅ Recorded {interaction_type} for {user_id}: {product_name}")
        return True

    def get_personalized_recommendations(self, user_id: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        The core engine: Iterates through all products and scores them for a specific user.
        
        Alternative: For a catalog of 1 million products, fetching all products 
        would be too slow. In that case, you would use a 'Candidate Generator' 
        (e.g., a vector search) to find the top 100 products first, then rank them.
        """
        if user_id not in self.user_profiles:
            print(f"⚠️ User {user_id} not found")
            return []

        user_profile = self.user_profiles[user_id]
        preferences = user_profile.get("preferences", {})

        try:
            products = self.client.collections.get("Product")

            # Fetch a broad set of candidates to rank
            response = products.query.fetch_objects(limit=100)
            all_products = [obj.properties for obj in response.objects]

            # Calculate a unique score for every product for this specific user
            scored_products = []
            for product in all_products:
                score = self._calculate_recommendation_score(product, preferences, user_profile)
                scored_products.append((score, product))

            # Sort products so the highest scores (best matches) are at the top
            scored_products.sort(key=lambda x: x[0], reverse=True)

            # Return only the top 'limit' recommendations
            recommendations = [product for _, product in scored_products[:limit]]

            print(f"✅ Generated {len(recommendations)} personalized recommendations for {user_id}")
            return recommendations

        except Exception as e:
            print(f"❌ Error generating recommendations: {e}")
            return []
    
    def _calculate_recommendation_score(self, product: Dict[str, Any], preferences: Dict[str, Any], user_profile: Dict[str, Any]) -> float:
        """
        The 'Secret Sauce' math. We weight different factors differently.
        
        Weights Used:
        - Category: 30% (If you like shoes, we show you shoes)
        - Budget: 25% (If you can't afford it, it's not a good rec)
        - Rating: 20% (Quality matters)
        - Brand: 15% (Brand loyalty)
        - Availability: 10% (Don't recommend out-of-stock items)
        """
        score = 0.0
        
        # 1. Category preference (The strongest indicator)
        preferred_categories = preferences.get("preferred_categories", [])
        if preferred_categories and product.get("category") in preferred_categories:
            score += 30
        
        # 2. Budget range (Ensures price relevance)
        budget_range = preferences.get("budget_range")
        if budget_range and self._is_in_budget(product.get("price", 0), budget_range):
            score += 25
        
        # 3. Social Proof (Higher ratings = more trust)
        if product.get("rating", 0) >= 4.0:
            score += 20
        elif product.get("rating", 0) >= 3.0:
            score += 10
        
        # 4. Brand Loyalty
        preferred_brands = preferences.get("preferred_brands", [])
        if preferred_brands and product.get("brand") in preferred_brands:
            score += 15
        
        # 5. Inventory Status (Recency/Availability bonus)
        if product.get("in_stock"):
            score += 10
        
        # 6. Interaction Penalty: Don't show the user the same things 
        # they've already looked at but didn't buy.
        for interaction in user_profile.get("interaction_history", []):
            if interaction.get("product_name") == product.get("name") and interaction.get("type") != "purchase":
                score -= 5
        
        return score
    
    @staticmethod
    def _is_in_budget(price: float, budget_range: str) -> bool:
        """Check if price is within budget range"""
        try:
            parts = budget_range.split("-")
            if len(parts) == 2:
                min_price = float(parts[0])
                max_price = float(parts[1])
                return min_price <= price <= max_price
        except:
            pass
        return False
    
    def get_user_profile(self, user_id: str) -> Dict[str, Any]:
        """Get user profile"""
        if user_id in self.user_profiles:
            return self.user_profiles[user_id]
        return None
    
    def get_interaction_summary(self, user_id: str) -> Dict[str, Any]:
        """Get summary of user interactions"""
        if user_id not in self.user_profiles:
            return None
        
        profile = self.user_profiles[user_id]
        interactions = profile.get("interaction_history", [])
        
        summary = {
            "total_interactions": len(interactions),
            "interaction_types": {},
            "products_viewed": set(),
            "last_interaction": interactions[-1] if interactions else None
        }
        
        for interaction in interactions:
            itype = interaction.get("type")
            summary["interaction_types"][itype] = summary["interaction_types"].get(itype, 0) + 1
            summary["products_viewed"].add(interaction.get("product_name"))
        
        summary["products_viewed"] = list(summary["products_viewed"])
        return summary

