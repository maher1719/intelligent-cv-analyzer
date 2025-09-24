# app.py
import streamlit as st
import pandas as pd
import os
import warnings
from utils import get_text_from_file
from analytics import SkillAnalytics
from parser import DocumentParser
from analyzer import CVAnalyzer

# Suppress common warnings
warnings.filterwarnings('ignore')

# --- CONFIGURATION ---
CO_OCCURRENCE_FILE = 'csv/correspendentFinalCleanTranspose.csv'
CLUSTERS_FILE = 'csv/skill_clusters.csv'
CENTRALITY_FILE = 'csv/centrality_measures.csv'
KNOWLEDGE_BASE_FILE  =  'csv/skill_knowledge_base2.csv'  # <-- ADD THIS LINE
# --- DATA LOADING (Cached for performance) ---
# ... (keep all the code above this function) ...

# --- DATA LOADING (Cached for performance) ---
@st.cache_data
def load_analytics_data():
    """Loads and prepares all analysis data. This is the definitive version."""
    try:
        # Check for file existence
        required_files = [CO_OCCURRENCE_FILE, CLUSTERS_FILE, CENTRALITY_FILE, KNOWLEDGE_BASE_FILE]
        for f in required_files:
            if not os.path.exists(f):
                st.error(f"Missing essential data file: '{f}'. Please run the data generation scripts.")
                return None

        # 1. Co-occurrence Matrix
        co_occurrence_matrix = pd.read_csv(CO_OCCURRENCE_FILE, index_col=0)
        co_occurrence_matrix.index = co_occurrence_matrix.index.str.lower().str.strip()
        co_occurrence_matrix.columns = co_occurrence_matrix.columns.str.lower().str.strip()
        if co_occurrence_matrix.index.name is None or co_occurrence_matrix.index.name == 'unnamed: 0':
            co_occurrence_matrix.index.name = 'skill'

        # 2. Skill Clusters
        skill_clusters = pd.read_csv(CLUSTERS_FILE)
        skill_clusters.columns = [col.lower().strip() for col in skill_clusters.columns] # Force lowercase
        skill_clusters.set_index('skill', inplace=True)
        
        # 3. Centrality Scores
        centrality_scores = pd.read_csv(CENTRALITY_FILE)
        centrality_scores.columns = [col.lower().strip() for col in centrality_scores.columns] # Force lowercase
        centrality_scores.set_index('skill', inplace=True)
        
        # 4. Skill Knowledge Base (Using the headers you provided)
        skill_knowledge_base = pd.read_csv(KNOWLEDGE_BASE_FILE)
        # Force all column names to lowercase to prevent any case issues
        skill_knowledge_base.columns = [col.lower().strip() for col in skill_knowledge_base.columns]
        # Set the index to 'canonical_skill' for fast lookups
        skill_knowledge_base.set_index('canonical_skill', inplace=True)

        print("All analytics data loaded and standardized successfully.")
        
        # Instantiate the analytics engine with the loaded data
        return SkillAnalytics(
            co_occurrence_matrix, 
            skill_clusters, 
            centrality_scores, 
            skill_knowledge_base
        )
        
    except Exception as e:
        st.error(f"FATAL ERROR during data loading: {e}")
        st.error("Please ensure all your CSV files are correctly formatted and in your project folder.")
        st.stop()

# --- INITIALIZE THE APP ---
st.set_page_config(layout="wide", page_title="AI CV Potential Seeker")
analytics_engine = load_analytics_data() # This call remains the same

# ... (the rest of your app.py code remains the same) ...
# --- INITIALIZE THE APP ---
st.set_page_config(layout="wide", page_title="AI CV Potential Seeker")
analytics_engine = load_analytics_data()

# --- UI ---
st.title("👨‍💻 AI CV Potential Seeker")
st.markdown("An intelligent tool to analyze candidate potential beyond simple keyword matching.")

# --- SIDEBAR ---
st.sidebar.title("Configuration")
api_key = st.sidebar.text_input("Enter your Google Gemini API Key", type="password")
st.sidebar.markdown("[Get your free API key from Google AI Studio](https://aistudio.google.com/app/apikey)")

# --- DEMO MODE TOGGLE ---
# If the analytics engine failed to load, force demo mode.
if analytics_engine is None:
    st.sidebar.warning("Local data files not found. Running in **Demo Mode (AI-Only)**.")
    is_demo_mode = True
else:
    is_demo_mode = st.sidebar.checkbox("Run in Demo Mode (AI-Only Analysis)", value=False, help="If checked, the app will only use the Gemini API for analysis and will not use the local, data-driven skill models.")

# Initialize Parser and Analyzer based on mode
doc_parser = None
cv_analyzer = None
if api_key:
    doc_parser = DocumentParser(api_key=api_key)
    if doc_parser.model:
        # Pass the analytics_engine only if we are NOT in demo mode
        engine_to_use = None if is_demo_mode else analytics_engine
        cv_analyzer = CVAnalyzer(ai_model=doc_parser.model, analytics_engine=engine_to_use)

# --- MAIN PAGE LAYOUT ---
col1, col2 = st.columns(2)
with col1:
    st.header("1. Upload Candidate's CV")
    uploaded_file = st.file_uploader("Upload a PDF or DOCX file", type=['pdf', 'docx'], label_visibility="collapsed")
with col2:
    st.header("2. Paste Job Description")
    job_description_text = st.text_area("Paste the full job description here", height=300, placeholder="e.g., We are looking for a Senior Python developer...")

if st.button("Analyze Now", type="primary", use_container_width=True, disabled=(not cv_analyzer)):
    if not cv_analyzer:
        st.error("Please enter a valid Google Gemini API Key in the sidebar.")
    elif uploaded_file and job_description_text:
        with st.spinner("AI is processing documents and running analysis..."):
            cv_text = get_text_from_file(uploaded_file)
            
            # The list of skills for the parser needs to come from the engine, or be empty in demo mode
            skill_list = analytics_engine.all_skills if not is_demo_mode and analytics_engine else []

            if cv_text and doc_parser:
                cv_data = doc_parser.get_structured_data(cv_text, skill_list)
                job_data = doc_parser.get_structured_data(job_description_text, skill_list)

                if cv_data and job_data:
                    results = cv_analyzer.analyze(cv_data, job_data)
                    
                    st.markdown("---")
                    st.header("🚀 Candidate Evaluation Report")
                    st.markdown(results['ai_report'])
                    
                    # Only show the detailed breakdown if NOT in demo mode
                    if not cv_analyzer.is_demo_mode:
                        with st.expander("Show Data-Driven Metrics and Details"):
                            # ... (The rest of your display logic for scores and skill lists)
                            st.subheader("Quantitative Scores")
                            metric1, metric2 = st.columns(2)
                            metric1.metric(label="Weighted Skill Match", value=f"{results['weighted_score']:.1f}%", help="Weighted by market importance of skills.")
                            metric2.metric(label="Domain Fit", value=f"{results['domain_fit_score']:.1f}%", help=results['domain_justification'])
                            st.subheader("Skill Breakdown")
                            # ... etc.

                else:
                    st.error("AI parsing failed. Please check the document contents or API key.")
    else:
        st.warning("Please upload a CV and paste a job description.")