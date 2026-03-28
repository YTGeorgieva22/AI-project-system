import sys
import os
from routes import main_routes

# allow imports from parent folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from flask import Flask, render_template
from weaviate_client import weaviate_manager
from schema import setup_collections
from data_loader import DataLoader
from query_agent import QueryAgent
from personalization import PersonalizationAgent
from transformation import TransformationAgent


def create_app():
    """
    Factory function to create and configure the Flask application.
    Initializes the Weaviate connection, seeds data, and attaches 
    agents to the app configuration.

    Returns:
        Flask: The configured Flask application instance.
    """
    app = Flask(__name__)

    # Establish connection to Weaviate Cloud
    weaviate_manager.connect()
    client = weaviate_manager.get_client()

    # Ensure necessary collections exist
    setup_collections(client)

    # Seed the database with sample products and reviews
    loader = DataLoader(client)
    loader.load_all_data()

    # Attach initialized agents to the app config for access in routes
    app.config["query_agent"] = QueryAgent(client)
    app.config["personalization_agent"] = PersonalizationAgent(client)
    app.config["transformation_agent"] = TransformationAgent(client)

    # Register application blueprints/routes
    app.register_blueprint(main_routes, prefix="/main")

    return app


if __name__ == "__main__":
    # Create the app and run it in debug mode for development
    app = create_app()
    app.run(debug=True)