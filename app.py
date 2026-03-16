import streamlit as st
import json
import pandas as pd
from agent import ResearcherAgent
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="Financial Researcher Agent",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark theme and styling
st.markdown("""
<style>
    .reportview-container {
        background: #1e1e1e
    }
    .main {
        background-color: #121212;
        color: #e0e0e0;
    }
    .stTextInput>div>div>input {
        background-color: #2b2b2b;
        color: white;
    }
    /* Simple dynamic button */
    .stButton>button {
        background-color: #007bff;
        color: white;
        border-radius: 4px;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #0056b3;
    }
</style>
""", unsafe_allow_html=True)

st.title("📈 Free Financial Researcher Agent")
st.markdown("**100% Free Stack:** DuckDuckGo Search, OpenRouter (DeepSeek/Llama), FAISS, Streamlit")

@st.cache_resource
def get_agent():
    return ResearcherAgent()

agent = get_agent()

query = st.text_input("Enter your financial query (e.g. 'PSX crash analysis March 2026')", value="")

def run_research():
    if not query:
        st.warning("Please enter a query.")
        return
        
    with st.spinner("Initializing Research Pipeline..."):
        # 1. Search DB
        progress = st.progress(10)
        st.info("Querying DuckDuckGo & Semantic Cache...")
        
        # Fast forward progress to mock steps visually
        progress.progress(40)
        st.info("Scoring Credibility of Sources...")
        
        progress.progress(70)
        st.info("Extracting Key Facts via OpenRouter LLM...")
        
        try:
            result = agent.run(query)
            progress.progress(100)
            st.success(f"Analysis Complete! (Confidence: {result['confidence']:.2f})")
            
            # Display Results visually
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.subheader("Extracted Key Facts")
                for fact in result['key_facts']:
                    st.markdown(f"- **{fact}**")
                    
                st.subheader("Sources Ranked by Credibility")
                if result['sources']:
                    df = pd.DataFrame(result['sources'])
                    df = df[['title', 'credibility_score', 'recency_score', 'url', 'snippet']]
                    st.dataframe(df, use_container_width=True)
                else:
                    st.write("No specific sources evaluated in this step.")
                    
            with col2:
                st.subheader("Raw JSON Output")
                json_data = json.dumps(result, indent=2)
                st.code(json_data, language="json")
                
                st.download_button(
                    label="Download JSON",
                    data=json_data,
                    file_name="research_report.json",
                    mime="application/json"
                )
        except Exception as e:
            st.error(f"Error during research: {str(e)}")

if st.button("Run Research"):
    run_research()

st.sidebar.markdown("### Settings")
st.sidebar.markdown("Ensure `.env` contains `OPENROUTER_API_KEY`.")
if not agent.api_key:
    st.sidebar.error("Missing OpenRouter API Key. Add to .env and restart.")
else:
    st.sidebar.success("API Key Found!")
    
st.sidebar.markdown("### Agent Architecture")
st.sidebar.markdown("""
1. **Search**: DuckDuckGo
2. **Local Score**: Domain & Recency rules
3. **LLM**: Free OpenRouter Models
4. **Cache**: Local FAISS index
""")
