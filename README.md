# Free Financial Researcher Agent

A production-ready Financial Researcher Agent built entirely on **FREE** tools and APIs.

## 🌟 Features
- **Zero API Costs**: Uses OpenRouter's free tier (Llama 3.2 / DeepSeek), DuckDuckGo Search, and HuggingFace models.
- **Local Credibility Scoring**: Robust local domain rules and recency evaluation.
- **Semantic Caching**: Local vector store using FAISS & `sentence-transformers` for instant cached responses without calling the API.
- **Streamlit UI**: Clean, responsive frontend designed for Streamlit Cloud deployment.

## 🚀 Quick Setup (MS AI Student-Proof)

### 1. Local Installation
Make sure you have Python 3.10+ installed.

1. Clone or download this repository.
2. Install the free dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Get your **Free API Key**:
   - Go to [OpenRouter.ai](https://openrouter.ai/)
   - Create a free account and generate an API key.
4. Setup environment variables:
   ```bash
   cp .env.example .env
   # Open .env and paste your OPENROUTER_API_KEY
   ```
5. Run the interface locally:
   ```bash
   streamlit run app.py
   ```

---

### 2. 🌍 One-Click Deployment (FREE Streamlit Cloud)

Deploy this app to the public web in 3 minutes for free, forever:

1. Push this folder to a new **GitHub Repository**.
2. Go to [share.streamlit.io](https://share.streamlit.io/) and log in with GitHub.
3. Click **New app** -> From existing repository.
4. Select your newly created repo and branch.
5. Set the **Main file path** to `app.py`.
6. Click **Advanced Settings** -> Paste your `OPENROUTER_API_KEY=your_key_here` into the **Secrets** box.
7. Click **Deploy!**

Your agent is now live! 

---

### 3. 🐳 Docker Deployment
```bash
docker build -t researcher-agent .
docker run -p 8501:8501 --env-file .env researcher-agent
```

## Example Query
> *"PSX crash analysis March 2026"*

Output is structurally clean JSON containing key facts, a confidence score, and fully attributed real-time sources!
