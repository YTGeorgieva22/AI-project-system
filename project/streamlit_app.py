"""
Streamlit web interface for the E-Commerce Assistant
"""
import streamlit as st
from weaviate_client import weaviate_manager
from schema import setup_collections
from data_loader import DataLoader
from query_agent import QueryAgent
from personalization import PersonalizationAgent
from transformation import TransformationAgent


def initialize_session_state():
    """
    Initializes the Streamlit session state variables to maintain application 
    context across re-renders.
    """
    if 'initialized' not in st.session_state:
        st.session_state.initialized = False
        st.session_state.client = None
        st.session_state.query_agent = None
        st.session_state.personalization_agent = None
        st.session_state.transformation_agent = None
        st.session_state.current_user = None


def initialize_app():
    """
    Bootstraps the backend components if they haven't been initialized yet.
    This includes connecting to Weaviate and setting up agents.
    
    Returns:
        bool: True if the app was successfully initialized.
    """
    if not st.session_state.initialized:
        # Connect to Weaviate
        if not weaviate_manager.connect():
            st.error("Failed to connect to Weaviate. Check your configuration.")
            return False
        
        st.session_state.client = weaviate_manager.get_client()
        
        # Setup collections
        setup_collections(st.session_state.client)
        
        # Initialize agents
        data_loader = DataLoader(st.session_state.client)
        data_loader.load_all_data()
        
        st.session_state.query_agent = QueryAgent(st.session_state.client)
        st.session_state.personalization_agent = PersonalizationAgent(st.session_state.client)
        st.session_state.transformation_agent = TransformationAgent(st.session_state.client)
        st.session_state.initialized = True
    
    return True


def main():
    """
    The main entry point for the Streamlit application. Defines the layout, 
    navigation, and page-specific logic.
    """
    st.set_page_config(
        page_title="🛍️ E-Commerce Assistant",
        page_icon="🛍️",
        layout="wide"
    )
    
    # Initialize session state
    initialize_session_state()
    
    # Sidebar
    with st.sidebar:
        st.title("🛍️ E-Commerce Assistant")
        st.write("Powered by Weaviate Agents")
        
        page = st.radio("Select Page", [
            "🏠 Home",
            "❓ Query Agent",
            "🎯 Personalization",
            "🔄 Transformation",
            "📊 Demo Queries"
        ])
    
    # Initialize app
    if not initialize_app():
        return
    
    # Home page
    if page == "🏠 Home":
        st.title("Welcome to E-Commerce Assistant")
        st.write("""
        This application demonstrates Weaviate Agents for e-commerce:
        
        **Collections:**
        - 📦 **Products**: Catalog of electronics, sports, and food items
        - 💬 **Reviews**: Customer reviews and feedback
        
        **Features:**
        - 🤖 **Query Agent**: Natural language questions about products
        - 🎯 **Personalization**: User profiles and personalized recommendations
        - 🔄 **Transformation**: Data enrichment and enhancement
        """)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Products", "6")
            st.metric("Reviews", "8")
        with col2:
            st.metric("Categories", "3")
            st.metric("Brands", "6")
    
    # Query Agent page
    elif page == "❓ Query Agent":
        st.title("Query Agent - Ask Questions")
        st.write("Ask natural language questions about products and reviews")
        
        query = st.text_area(
            "Your question:",
            placeholder="E.g., 'What headphones do you recommend?'"
        )
        
        if st.button("Ask", use_container_width=True):
            if query:
                with st.spinner("Processing..."):
                    result = st.session_state.query_agent.ask(query)
                
                if result.get('success'):
                    st.success("Answer:")
                    st.write(result['answer'])
                else:
                    st.error("Error processing query")
    
    # Personalization page
    elif page == "🎯 Personalization":
        st.title("Personalization Agent")
        
        tab1, tab2 = st.tabs(["Create Persona", "Get Recommendations"])
        
        with tab1:
            st.subheader("Create User Persona")
            
            user_id = st.text_input("User ID")
            
            col1, col2 = st.columns(2)
            with col1:
                preferred_categories = st.multiselect(
                    "Preferred Categories",
                    ["Electronics", "Sports & Outdoors", "Food & Beverages"]
                )
            with col2:
                budget_range = st.text_input("Budget Range (e.g., '50-200')")
            
            preferred_brands = st.multiselect(
                "Preferred Brands",
                ["AudioTech", "HydroFlask", "RunPro", "TechWear", "TeaLeaf", "PowerHub"]
            )
            
            if st.button("Create Persona", use_container_width=True):
                if user_id:
                    preferences = {
                        "preferred_categories": preferred_categories,
                        "budget_range": budget_range,
                        "preferred_brands": preferred_brands
                    }
                    st.session_state.personalization_agent.create_user_persona(user_id, preferences)
                    st.success(f"✅ Persona created for {user_id}")
                    st.session_state.current_user = user_id
        
        with tab2:
            st.subheader("Get Personalized Recommendations")
            
            user_id = st.text_input("User ID", value=st.session_state.current_user or "")
            
            if st.button("Get Recommendations", use_container_width=True):
                if user_id:
                    with st.spinner("Generating recommendations..."):
                        recs = st.session_state.personalization_agent.get_personalized_recommendations(user_id)
                    
                    if recs:
                        st.success(f"Found {len(recs)} recommendations")
                        for product in recs:
                            col1, col2 = st.columns([3, 1])
                            with col1:
                                st.write(f"**{product['name']}**")
                                st.write(f"{product.get('description', '')[:200]}...")
                            with col2:
                                st.write(f"${product['price']}")
                                st.write(f"⭐ {product['rating']}/5")
    
    # Transformation page
    elif page == "🔄 Transformation":
        st.title("Transformation Agent")
        st.write("Enrich product data with additional information")
        
        tab1, tab2 = st.tabs(["Add Summary", "Add Tags"])
        
        with tab1:
            st.subheader("Add Product Summary")
            product_name = st.selectbox(
                "Select Product",
                ["Wireless Bluetooth Headphones", "Stainless Steel Water Bottle", 
                 "Lightweight Running Shoes", "Smart Watch Pro", "Organic Green Tea Set", 
                 "Portable Phone Charger"]
            )
            
            summary = st.text_area("Summary", placeholder="Enter product summary")
            
            if st.button("Add Summary", use_container_width=True):
                if summary:
                    st.session_state.transformation_agent.add_product_summary(product_name, summary)
                    st.success("✅ Summary added")
        
        with tab2:
            st.subheader("Add Product Tags")
            product_name = st.selectbox(
                "Select Product",
                ["Wireless Bluetooth Headphones", "Stainless Steel Water Bottle", 
                 "Lightweight Running Shoes", "Smart Watch Pro", "Organic Green Tea Set", 
                 "Portable Phone Charger"],
                key="product_tags"
            )
            
            tags = st.text_input("Tags (comma-separated)")
            
            if st.button("Add Tags", use_container_width=True):
                if tags:
                    tags_list = [t.strip() for t in tags.split(",")]
                    st.session_state.transformation_agent.add_product_tags(product_name, tags_list)
                    st.success("✅ Tags added")
    
    # Demo Queries page
    elif page == "📊 Demo Queries":
        st.title("Demo Queries")
        st.write("Pre-configured queries demonstrating different capabilities")
        
        demos = [
            ("Simple Product Search", "What headphones do you recommend for music lovers?"),
            ("Category & Price Filter", "Show me all electronics under $100"),
            ("Aggregation Query", "What products have the best ratings?"),
            ("Multi-Collection", "Tell me about running shoes and what customers think"),
            ("Complex Filter", "Is there anything in sports and outdoors category with good reviews?"),
        ]
        
        for title, query in demos:
            with st.expander(f"📋 {title}"):
                st.write(f"**Query:** {query}")
                
                if st.button("Run", key=query):
                    with st.spinner("Processing..."):
                        result = st.session_state.query_agent.ask(query)
                    
                    if result.get('success'):
                        st.write(result['answer'])
                    else:
                        st.error("Error processing query")


if __name__ == "__main__":
    main()

