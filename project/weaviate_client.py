"""
Weaviate client initialization with support for Agents
"""
import os
from dotenv import load_dotenv
import weaviate
from weaviate.classes.init import Auth

load_dotenv()

class WeaviateClientManager:
    """
    Manages the lifecycle of the connection to Weaviate Cloud.
    
    Why use a Manager?
    Establishing a connection to a cloud database is 'expensive' in terms of 
    time and resources. This manager ensures we connect once and reuse that 
    connection across the whole app.
    """
    
    def __init__(self):
        # Pulling secrets from .env file for security.
        self.url = os.getenv("WEAVIATE_URL")
        self.api_key = os.getenv("WEAVIATE_API_KEY")
        self.openai_key = os.getenv("OPENAI_API_KEY")
        self.client = None
    
    def connect(self):
        """
        Establishes the link between your Python code and the Cloud Vector DB.
        """
        try:
            if not self.url or not self.api_key:
                print("❌ Error: WEAVIATE_URL and WEAVIATE_API_KEY environment variables are required")
                return False
            
            # Connect to Weaviate Cloud using the API Key.
            # We also pass the OpenAI key in the 'headers'. 
            # This allows Weaviate to talk to OpenAI on our behalf for vectorization.
            self.client = weaviate.connect_to_weaviate_cloud(
                cluster_url=self.url,
                auth_credentials=Auth.api_key(self.api_key),
                headers={
                    "X-OpenAI-Api-Key": self.openai_key
                }
            )
            
            # Check if the database is awake and ready to receive queries.
            if self.client.is_ready():
                print(f"✅ Connected to Weaviate Cloud at {self.url}")
                return True
            else:
                print("❌ Weaviate Cloud is not ready")
                return False
                
        except Exception as e:
            print(f"❌ Failed to connect to Weaviate Cloud: {e}")
            return False
    
    def get_client(self):
        """
        Retrieves the active Weaviate client, establishing a connection if one doesn't exist.
        
        Returns:
            The Weaviate client instance.
        """
        if self.client is None:
            self.connect()
        return self.client
    
    def close(self):
        """
        Gracefully closes the connection to the Weaviate Cloud instance.
        """
        if self.client:
            self.client.close()
            print("Connection closed")
    
    def __enter__(self):
        """
        Context manager entry point: establishes the connection.
        
        Returns:
            The established Weaviate client.
        """
        self.connect()
        return self.client
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Context manager exit point: ensures the connection is closed.
        """
        self.close()


# Global client instance
weaviate_manager = WeaviateClientManager()

