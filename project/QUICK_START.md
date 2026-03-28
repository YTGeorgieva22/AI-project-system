# 🚀 QUICK START GUIDE

## Project: Weaviate E-Commerce Agents Application

This guide will get you running in **5 minutes**.

---

## ✅ Prerequisites Check

```bash
# Check Python version (3.8+)
python --version

# Check pip
pip --version
```

---

## 📋 Step 1: Setup Environment Variables

Edit `.env` file in project root:

```env
# Get from Weaviate Cloud Console: https://console.weaviate.cloud
WEAVIATE_URL=https://your-cluster-name.weaviate.network
WEAVIATE_API_KEY=your-api-key-here

# Get from OpenAI: https://platform.openai.com/api-keys  
OPENAI_API_KEY=your-openai-key-here

DEBUG=False
```

**How to find your credentials:**

1. **Weaviate Cloud URL & API Key:**
   - Go to https://console.weaviate.cloud
   - Sign in or create account
   - Create a cluster or select existing one
   - Copy the **Cluster URL** (format: `https://cluster-name.weaviate.network`)
   - Copy the **API Key**

2. **OpenAI API Key:**
   - Go to https://platform.openai.com/api-keys
   - Create new secret key
   - Copy the key

---

## 🔧 Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

✅ You should see: `Successfully installed weaviate-client streamlit python-dotenv...`

---

## ▶️ Step 3: Run the Application

### Option A: CLI Mode (Recommended for First Time)

```bash
python app.py
```

You'll see a menu:
```
┌─────────────────────────────────────┐
│         MAIN MENU                    │
├─────────────────────────────────────┤
│ 1. Run Demo Queries (5 types)       │
│ 2. Personalization Agent Demo       │
│ 3. Transformation Agent Demo        │
│ 4. Interactive Mode                 │
│ 5. Run All Demos                    │
└─────────────────────────────────────┘

Select option (1-5): 
```

**Try each option:**
- **Option 1:** See 5 different query examples
- **Option 2:** Create user personas and get recommendations
- **Option 3:** Enrich product data
- **Option 4:** Ask questions yourself (type "help" for commands)
- **Option 5:** Run everything

### Option B: Web Interface

```bash
streamlit run streamlit_app.py
```

Opens at: http://localhost:8501

Use sidebar to navigate: Home, Query Agent, Personalization, Transformation, Demo Queries

---

## 🎯 First Query Examples

Once running in **Interactive Mode** (Option 4), try these:

```
You: What headphones do you recommend?
Assistant: [Lists products with ratings and descriptions]

You: Show me electronics under $100
Assistant: [Filtered results]

You: Tell me about running shoes and customer feedback
Assistant: [Products + Reviews combined]

You: help
Assistant: [Shows available commands]

You: categories
Assistant: [Shows available categories]

You: quit
Assistant: [Exit]
```

---

## 📊 What You'll See

### Demo Queries Output:
```
Query 1: Simple Product Search
Question: What headphones do you recommend for music lovers?
──────────────────────────────────────
Answer:
📦 Matching Products:
1. Wireless Bluetooth Headphones ($149.99)
   Brand: AudioTech | Category: Electronics
   Rating: ⭐ 4.5/5 (234 reviews)
   In Stock: ✅ Yes
   Description: High-quality wireless headphones...
```

### Personalization Output:
```
👤 Creating user personas...
✅ Created persona for user: user_001
   Preferences: {'preferred_categories': ['Electronics'], ...}

💡 Generating personalized recommendations...
For User 001:
  1. Wireless Bluetooth Headphones ($149.99) - ⭐ 4.5
  2. Smart Watch Pro ($299.99) - ⭐ 4.4
  3. Portable Phone Charger ($39.99) - ⭐ 4.3
```

---

## ⚠️ Troubleshooting

### Issue: "WEAVIATE_URL and WEAVIATE_API_KEY not set"

**Solution:**
1. Check `.env` file exists in project root
2. Make sure you've filled in actual credentials (not placeholders)
3. Restart the app

### Issue: "Weaviate Cloud is not ready"

**Solution:**
1. Check your Weaviate cluster is running: https://console.weaviate.cloud
2. Verify URL format: `https://cluster-name.weaviate.network` (no trailing slash)
3. Check API key is correct

### Issue: "ModuleNotFoundError: No module named 'weaviate'"

**Solution:**
```bash
pip install -r requirements.txt
```

### Issue: "OpenAI API error"

**Solution:**
1. Check your OpenAI API key is correct
2. Verify API key has access: https://platform.openai.com/account/billing/limits
3. Check you have credits available

---

## 📁 Project Files

```
project/
├── app.py                    # Main CLI - RUN THIS
├── streamlit_app.py          # Web interface
├── query_agent.py            # Answers questions
├── personalization.py        # Recommendations
├── transformation.py         # Data enrichment
├── data_loader.py            # Sample data
├── weaviate_client.py        # Weaviate connection
├── schema.py                 # Data structure
├── .env                      # YOUR CONFIG (edit this!)
├── requirements.txt          # Dependencies
├── README.md                 # Full documentation
├── TECHNICAL_REPORT.md       # Detailed technical info
└── QUICK_START.md            # This file
```

---

## 🎓 Learning Path

1. **First Run:** Execute Option 1 (Demo Queries)
   - See what the system can do

2. **Try Interactive:** Select Option 4
   - Ask your own questions
   - Use "categories" command to explore

3. **Explore Features:** Try Options 2 & 3
   - See personalization in action
   - Learn data enrichment

4. **Read Docs:**
   - README.md - Overview
   - TECHNICAL_REPORT.md - Deep dive

5. **Explore Code:**
   - query_agent.py - How queries work
   - personalization.py - How recommendations work
   - app.py - Main flow

---

## 📚 Available Data

**6 Products:**
1. Wireless Bluetooth Headphones ($149.99)
2. Stainless Steel Water Bottle ($34.99)
3. Lightweight Running Shoes ($129.99)
4. Smart Watch Pro ($299.99)
5. Organic Green Tea Set ($49.99)
6. Portable Phone Charger ($39.99)

**8 Reviews** linked to products

**3 Categories:**
- Electronics
- Sports & Outdoors
- Food & Beverages

---

## 🔗 Useful Links

- **Weaviate Cloud:** https://console.weaviate.cloud
- **OpenAI API:** https://platform.openai.com/api-keys
- **Weaviate Docs:** https://weaviate.io/developers/weaviate
- **Weaviate Agents:** https://docs.weaviate.io/agents

---

## ✅ Checklist

- [ ] .env file configured with credentials
- [ ] `pip install -r requirements.txt` ran successfully
- [ ] Can import weaviate, streamlit, pydantic
- [ ] `python app.py` starts without errors
- [ ] Can see the main menu
- [ ] Option 1 (Demo Queries) works
- [ ] Option 4 (Interactive) works
- [ ] Web interface runs with `streamlit run streamlit_app.py`

---

## 🎬 Next Steps

After Quick Start:
1. Read `README.md` for full feature overview
2. Check `TECHNICAL_REPORT.md` for architecture details
3. Explore the code in `app.py` and `query_agent.py`
4. Try modifying sample data in `data_loader.py`
5. Create your own demo queries

---

**Having issues?** Check the Troubleshooting section above!

**Ready to demo?** Press Enter and start exploring! 🚀

