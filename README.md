# AI-project-system

# 🛍️ Weaviate E-Commerce Agents Application

**An intelligent e-commerce assistant powered by Weaviate Agents** - demonstrating Query Agent, Personalization Agent, and Transformation Agent capabilities.

## 📋 Project Overview

This application showcases how to build an AI-powered e-commerce assistant using **Weaviate Agents** to:
- Answer natural language questions about products and reviews
- Provide personalized recommendations based on user profiles
- Enrich product data with summaries, tags, and insights

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment
Edit `.env` file with your credentials:
```env
WEAVIATE_URL=https://your-cluster.weaviate.network
WEAVIATE_API_KEY=your-api-key
OPENAI_API_KEY=your-openai-key
```

### 3. Run Application
```bash
# CLI Mode (Recommended for Demo)
python app.py

# Web Interface (Streamlit)
streamlit run streamlit_app.py
```

---

## 📊 Data Model

### Collections

**1. Product Collection** (6 products)
- name, description, price, category, brand, in_stock, rating, review_count
- Categories: Electronics, Sports & Outdoors, Food & Beverages

**2. Review Collection** (8 reviews)
- text, rating, product_name, reviewer_name, helpful_count, verified_purchase

---

## 🤖 Agents Implementation

### Query Agent
Answer natural language questions with:
- Single collection searches
- Multi-collection queries
- Category/price filtering
- Aggregation queries

**Demo Queries:**
1. "What headphones do you recommend?" (Simple search)
2. "Show me electronics under $100" (Filter)
3. "What products have best ratings?" (Aggregation)
4. "Tell me about running shoes and reviews" (Multi-collection)
5. "Sports items under $150 with good reviews?" (Complex)

### Personalization Agent
- Create user personas with preferences
- Track user interactions
- Generate personalized recommendations
- Scoring based on: category (30%), budget (25%), rating (20%), brand (15%), stock (10%)

### Transformation Agent
- Add product summaries
- Add keyword tags
- Add sentiment analysis
- Batch enrichment operations

---

## ✅ Features Implemented

- ✅ 2 Collections with meaningful data
- ✅ Query Agent with 5+ query types
- ✅ Personalization with user profiles
- ✅ Transformation agent for enrichment
- ✅ CLI interface with menu
- ✅ Streamlit web interface
- ✅ Interactive query mode
- ✅ Sample data (6 products, 8 reviews)
- ✅ Error handling
- ✅ Environment configuration

---

## 📁 Project Structure

```
project/
├── app.py                    # Main CLI application
├── streamlit_app.py          # Web interface
├── config.py                 # Configuration constants
├── weaviate_client.py        # Weaviate Cloud connection
├── schema.py                 # Collection schemas
├── data_loader.py            # Sample data
├── query_agent.py            # Query Agent
├── personalization.py        # Personalization Agent
├── transformation.py         # Transformation Agent
├── utils.py                  # Utilities
├── .env                      # Environment variables
├── requirements.txt          # Dependencies
└── README.md                 # This file
```

---

## 💻 Running Modes

### CLI Mode
```bash
python app.py
```
Options:
1. Run 5 Demo Queries
2. Personalization Agent Demo
3. Transformation Agent Demo
4. Interactive Query Mode
5. Run All Demos

### Interactive Mode
```bash
# After selecting option 4 in CLI
You: What headphones do you recommend?
Assistant: [Answer with product details]

Commands: help, categories, user:NAME, quit
```

### Web Interface
```bash
streamlit run streamlit_app.py
```
Pages: Home, Query Agent, Personalization, Transformation, Demo Queries

---

## 🔍 Sample Data

**Products:**
1. Wireless Bluetooth Headphones - $149.99 ⭐ 4.5
2. Stainless Steel Water Bottle - $34.99 ⭐ 4.8
3. Lightweight Running Shoes - $129.99 ⭐ 4.6
4. Smart Watch Pro - $299.99 ⭐ 4.4
5. Organic Green Tea Set - $49.99 ⭐ 4.9
6. Portable Phone Charger - $39.99 ⭐ 4.3

**Reviews:** 8 verified customer reviews with ratings and feedback

---

## 🔧 Troubleshooting

| Error | Solution |
|-------|----------|
| API key not set | Check `.env` file exists with credentials |
| Connection failed | Verify Weaviate URL and API key are correct |
| ModuleNotFoundError | Run `pip install -r requirements.txt` |
| OpenAI error | Verify OpenAI API key has access and credits |

---

## 📚 Documentation

For detailed technical documentation, see: `TECHNICAL_REPORT.md`

For Weaviate resources:
- [Weaviate Docs](https://weaviate.io/developers/weaviate)
- [Agents Docs](https://docs.weaviate.io/agents)

---

**Status:** ✅ Ready for Presentation  
**Version:** 1.0  
**Date:** March 2026

