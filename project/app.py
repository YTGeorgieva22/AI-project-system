"""
Main application with CLI interface
"""
import sys
from weaviate_client import weaviate_manager
from schema import setup_collections
from data_loader import DataLoader
from query_agent import QueryAgent
from personalization import PersonalizationAgent
from transformation import TransformationAgent
from utils import print_welcome, print_menu, format_response


class ECommerceAssistant:
    """
    The Orchestrator. 
    This class brings the Weaviate client, the Data Loader, and all 
    three Agents together into a single cohesive application.
    """

    def __init__(self):
        """
        Initializes the ECommerceAssistant with empty placeholders for its core components.
        """
        self.client = None
        self.query_agent = None
        self.personalization_agent = None
        self.transformation_agent = None
        self.data_loader = None
        self.current_user = None

    def initialize(self) -> bool:
        """
        Sets up the environment. 
        1. Connects to Weaviate Cloud.
        2. Creates the database schema (Collections).
        3. Wires up all the agents (Query, Personalization, Transformation).
        
        Returns:
            bool: True if initialization was successful, False otherwise.
        """
        print("\n🚀 Initializing E-Commerce Assistant...\n")

        # Connect to Weaviate using the manager
        if not weaviate_manager.connect():
            return False

        self.client = weaviate_manager.get_client()

        # Setup collections in the database
        if not setup_collections(self.client):
            print("⚠️  Collections setup failed or already exist")

        # Dependency Injection: We pass the same client to every agent 
        # so they all 'see' the same data in real-time.
        self.data_loader = DataLoader(self.client)
        self.query_agent = QueryAgent(self.client)
        self.personalization_agent = PersonalizationAgent(self.client)
        self.transformation_agent = TransformationAgent(self.client)

        print("✅ Application initialized successfully\n")
        return True

    def load_sample_data(self) -> bool:
        """
        Triggers the DataLoader to seed the database with initial products and reviews.
        
        Returns:
            bool: True if data loading was successful.
        """
        print("Loading sample data...")
        return self.data_loader.load_all_data()

    def run_demo_queries(self) -> None:
        """
        Runs a suite of pre-defined test queries to demonstrate the Query Agent's 
        capabilities, including vector search, filtering, and multi-collection retrieval.
        """
        print("\n" + "=" * 70)
        print("📋 DEMO: 5 Different Query Examples")
        print("=" * 70)

        demo_queries = [
            {
                "query": "What headphones do you recommend for music lovers?",
                "description": "Simple product search (Uses Vector/BM25 relevance)"
            },
            {
                "query": "Show me all electronics under $100",
                "description": "Hybrid query (Category + Price filters)"
            },
            {
                "query": "What products have the best ratings?",
                "description": "Aggregation (Ranking products by rating score)"
            },
            {
                "query": "Tell me about running shoes and what customers think",
                "description": "Multi-collection (Pulling from both Product and Review tables)"
            },
            {
                "query": "Is there anything in sports and outdoors category with good reviews?",
                "description": "Complex intent (Multiple conditions)"
            },
        ]

        # Iterate through demo queries and display results
        for i, demo in enumerate(demo_queries, 1):
            print(f"\n{'─' * 70}")
            print(f"Query {i}: {demo['description']}")
            print(f"Question: {demo['query']}")
            print(f"{'─' * 70}")

            result = self.query_agent.ask(demo['query'])

            print(f"\nAnswer:")
            print(result['answer'])

    def run_personalization_demo(self) -> None:
        """
        Demonstrates the Personalization Agent by creating user personas, 
        recording interactions, and generating tailored recommendations.
        """
        print("\n" + "=" * 70)
        print("🎯 DEMO: Personalization Agent")
        print("=" * 70)

        # Define explicit user preferences for demonstration
        user1_prefs = {
            "preferred_categories": ["Electronics"],
            "budget_range": "100-300",
            "preferred_brands": ["AudioTech", "TechWear"]
        }

        user2_prefs = {
            "preferred_categories": ["Sports & Outdoors"],
            "budget_range": "30-150",
            "preferred_brands": ["RunPro", "HydroFlask"]
        }

        # Create personas in the agent
        print("\n👤 Creating user personas...\n")
        self.personalization_agent.create_user_persona("user_001", user1_prefs)
        self.personalization_agent.create_user_persona("user_002", user2_prefs)

        # Record various types of interactions to simulate user behavior
        print("\n📝 Recording user interactions...\n")
        self.personalization_agent.record_interaction("user_001", "Wireless Bluetooth Headphones", "view")
        self.personalization_agent.record_interaction("user_001", "Smart Watch Pro", "add_to_cart")
        self.personalization_agent.record_interaction("user_001", "Portable Phone Charger", "view")

        self.personalization_agent.record_interaction("user_002", "Lightweight Running Shoes", "purchase")
        self.personalization_agent.record_interaction("user_002", "Stainless Steel Water Bottle", "view")

        # Generate and display personalized recommendations
        print("\n💡 Generating personalized recommendations...\n")

        print("For User 001:")
        recs_user1 = self.personalization_agent.get_personalized_recommendations("user_001")
        for i, product in enumerate(recs_user1, 1):
            print(f"  {i}. {product['name']} (${product['price']}) - ⭐ {product['rating']}")

        print("\nFor User 002:")
        recs_user2 = self.personalization_agent.get_personalized_recommendations("user_002")
        for i, product in enumerate(recs_user2, 1):
            print(f"  {i}. {product['name']} (${product['price']}) - ⭐ {product['rating']}")

    def run_transformation_demo(self) -> None:
        """
        Demonstrates the Transformation Agent by enriching product data with 
        new summaries and tags, enhancing the searchable information.
        """
        print("\n" + "=" * 70)
        print("🔄 DEMO: Transformation Agent")
        print("=" * 70)

        print("\n✨ Enriching products with additional data...\n")

        # Dynamically add summaries and tags to existing products
        self.transformation_agent.add_product_summary(
            "Wireless Bluetooth Headphones",
            "Professional-grade wireless headphones featuring advanced noise cancellation technology and extended battery life. Ideal for audiophiles and frequent travelers."
        )

        self.transformation_agent.add_product_tags(
            "Smart Watch Pro",
            ["fitness", "wearable", "health-tracking", "waterproof", "smartwatch"]
        )

        self.transformation_agent.add_product_tags(
            "Stainless Steel Water Bottle",
            ["eco-friendly", "hydration", "durable", "sports", "travel"]
        )

        # Display the log of all transformations performed
        print("\n📊 Transformation Log:")
        for log_entry in self.transformation_agent.get_transformation_log():
            print(f"  ✓ {log_entry}")

    def interactive_mode(self) -> None:
        """
        Starts an interactive loop allowing users to type natural language 
        questions or specific commands directly into the console.
        """
        print("\n" + "=" * 70)
        print("🤖 Interactive Query Mode")
        print("=" * 70)
        print("Type 'help' for available commands, 'quit' to exit\n")

        while True:
            try:
                user_input = input("You: ").strip()

                if not user_input:
                    continue

                if user_input.lower() == 'quit':
                    print("\nGoodbye! 👋")
                    break

                if user_input.lower() == 'help':
                    self._show_help()
                    continue

                if user_input.lower() == 'categories':
                    self._show_categories()
                    continue

                if user_input.lower().startswith('user:'):
                    # Set the current user context for personalization
                    self.current_user = user_input.split(':', 1)[1].strip()
                    print(f"Current user set to: {self.current_user}")
                    continue

                # Process the natural language query using the Query Agent
                result = self.query_agent.ask(user_input)
                print(f"\nAssistant: {result['answer']}\n")

            except KeyboardInterrupt:
                print("\n\nGoodbye! 👋")
                break
            except Exception as e:
                print(f"Error: {e}")

    def _show_help(self) -> None:
        """
        Displays a list of available commands and example queries for 
        the interactive mode.
        """
        print("""
Available commands:
  help        - Show this help message
  categories  - Show available product categories
  user:NAME   - Set current user for personalization
  quit        - Exit the application

Or ask any natural language question about products and reviews!
Examples:
  - "What are the best headphones?"
  - "Show me electronics under $50"
  - "What do customers think about running shoes?"
        """)

    def _show_categories(self) -> None:
        """
        Fetches and displays all unique product categories currently stored 
        in the Weaviate database.
        """
        try:
            products = self.client.collections.get("Product")
            response = products.query.fetch_objects(limit=100)

            # Use a set to collect unique category names
            categories = set()
            for obj in response:
                if "category" in obj.properties:
                    categories.add(obj.properties["category"])

            print("\n📂 Available Categories:")
            for cat in sorted(categories):
                print(f"  • {cat}")
            print()
        except Exception as e:
            print(f"Error: {e}")

    def shutdown(self) -> None:
        """
        Cleans up resources and closes the database connection before exiting.
        """
        print("\n🛑 Shutting down...\n")
        weaviate_manager.close()
        print("✅ Goodbye!\n")


def main():
    """
    The main entry point for the application. Orchestrates initialization, 
    data loading, and user interaction.
    """
    print_welcome()

    app = ECommerceAssistant()

    # Initialize components and check for success
    if not app.initialize():
        print("Failed to initialize. Exiting.")
        return

    # Automatically seed the database with sample data
    app.load_sample_data()

    # Provide a simple CLI menu for the user
    print("""
    1. Demo Queries
    2. Personalization
    3. Transformation
    4. Interactive Mode
    5. Run All
    6. Launch Web App (Flask) 🌐
    """)

    choice = input("Select option (1-6): ").strip()

    try:
        # Route the user's choice to the appropriate method
        if choice == "1":
            app.run_demo_queries()
        elif choice == "2":
            app.run_personalization_demo()
        elif choice == "3":
            app.run_transformation_demo()
        elif choice == "4":
            app.interactive_mode()
        elif choice == "5":
            print("Running all demos...\n")
            app.run_demo_queries()
            app.run_personalization_demo()
            app.run_transformation_demo()
        elif choice == "6":
            # Lazy import to avoid unnecessary dependencies if not used
            from flask_app.app import create_app

            flask_app = create_app()
            flask_app.run(debug=True)
        else:
            print("Invalid option")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Ensure proper shutdown regardless of errors
        app.shutdown()


if __name__ == "__main__":
    main()

