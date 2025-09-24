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

# --- DATA LOADING (Moved to the main app script) ---
@st.cache_data
def load_analytics_data():
    """Loads and prepares all the analysis data from your CSV files."""
    try:
        co_occurrence_matrix = pd.read_csv(CO_OCCURRENCE_FILE, index_col=0)
        skill_clusters = pd.read_csv(CLUSTERS_FILE, index_col='Skill')
        centrality_scores = pd.read_csv(CENTRALITY_FILE, index_col='Skill')
        
        # Standardize all skill names to lowercase for consistent matching
        co_occurrence_matrix.index = co_occurrence_matrix.index.str.lower()
        co_occurrence_matrix.columns = co_occurrence_matrix.columns.str.lower()
        skill_clusters.index = skill_clusters.index.str.lower()
        centrality_scores.index = centrality_scores.index.str.lower()
        
        print("Analytics data loaded successfully.")
        return co_occurrence_matrix, skill_clusters, centrality_scores
        
    except FileNotFoundError as e:
        st.error(f"FATAL ERROR: Could not find a required data file: {e.filename}")
        st.error("Please make sure all your CSV files are in the same folder as this script.")
        st.stop() # Stop the app if essential data is missing

# --- INITIALIZE THE APP ---

st.set_page_config(layout="wide", page_title="AI CV Potential Seeker")

# Load data
co_occurrence_matrix, skill_clusters, centrality_scores = load_analytics_data()

# Instantiate the analytics engine with the pre-loaded data.
analytics_engine = SkillAnalytics(co_occurrence_matrix, skill_clusters, centrality_scores)

# --- UI ---
st.title("👨‍💻 AI CV Potential Seeker")
st.markdown("This tool provides a deep analysis of a candidate's CV against a job description, identifying not just direct matches but also hidden potential and transferable skills.")

# --- SIDEBAR ---
st.sidebar.title("Configuration")
st.sidebar.markdown("To use this app, you need a Google AI API Key.")
api_key = st.sidebar.text_input("Enter your Google Gemini API Key", type="password")
st.sidebar.markdown("[Get your free API key from Google AI Studio](https://aistudio.google.com/app/apikey)")

# Initialize Parser and Analyzer if API key is provided
doc_parser = None
cv_analyzer = None
if api_key:
    doc_parser = DocumentParser(api_key=api_key)
    if doc_parser.model:
        cv_analyzer = CVAnalyzer(analytics_engine, doc_parser.model)

# --- MAIN PAGE LAYOUT ---
col1, col2 = st.columns(2)

with col1:
    st.header("1. Upload Candidate's CV")
    uploaded_file = st.file_uploader("Upload a PDF or DOCX file", type=['pdf', 'docx'], label_visibility="collapsed")

with col2:
    st.header("2. Paste Job Description")
    job_description_text = st.text_area("Paste the full job description here", height=250, label_visibility="collapsed", placeholder="e.g., We are looking for a Senior Python developer with 5+ years of experience...")

if st.button("Analyze Now", type="primary", use_container_width=True, disabled=(not cv_analyzer)):
    if not cv_analyzer:
        st.error("Please enter a valid Google Gemini API Key in the sidebar to proceed.")
    elif uploaded_file and job_description_text:
        with st.spinner("AI is processing documents and running analysis... This may take a moment."):
            
            cv_text = get_text_from_file(uploaded_file)
            
            if cv_text and doc_parser:
                cv_data = doc_parser.get_structured_data(cv_text, analytics_engine.all_skills)
                job_data = doc_parser.get_structured_data(job_description_text, analytics_engine.all_skills)

                if cv_data and job_data:
                    analysis_results = cv_analyzer.analyze(cv_data, job_data)
                    
                    st.markdown("---")
                    st.header("🚀 Candidate Evaluation Report")
                    st.markdown(analysis_results['ai_report'])
                    
                    with st.expander("Show Detailed Skill Breakdown"):
                        st.success(f"✅ Matched Skills ({len(analysis_results['matched_skills'])}):")
                        st.write(f"`{', '.join(analysis_results['matched_skills'])}`")
                        
                        st.error(f"❌ Missing Skills ({len(analysis_results['missing_skills'])}):")
                        st.write(f"`{', '.join(analysis_results['missing_skills'])}`")

                        st.info(f"💡 Potential Skills ({len(analysis_results['potential_skills'])}):")
                        for skill, info in analysis_results['potential_skills'].items():
                            st.write(f"- Can likely learn **{skill.title()}** due to experience in `{info['proxy'].title()}`.")
                else:
                    st.error("AI parsing failed. This can happen due to API issues or if the documents are empty/unreadable. Please check the document contents or try again.")
    else:
        st.warning("Please upload a CV and provide a job description to analyze.")