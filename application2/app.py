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

# --- DATA LOADING (Cached for performance) ---
@st.cache_data
def load_analytics_data():
    """Loads and prepares all the analysis data from your CSV files."""
    try:
        co_occurrence_matrix = pd.read_csv(CO_OCCURRENCE_FILE, index_col=0)
        skill_clusters = pd.read_csv(CLUSTERS_FILE, index_col='Skill')
        centrality_scores = pd.read_csv(CENTRALITY_FILE, index_col='Skill')
        
        co_occurrence_matrix.index = co_occurrence_matrix.index.str.lower()
        co_occurrence_matrix.columns = co_occurrence_matrix.columns.str.lower()
        skill_clusters.index = skill_clusters.index.str.lower()
        centrality_scores.index = centrality_scores.index.str.lower()
        
        print("Analytics data loaded successfully.")
        return co_occurrence_matrix, skill_clusters, centrality_scores
        
    except FileNotFoundError as e:
        st.error(f"FATAL ERROR: Could not find a required data file: {e.filename}")
        st.error(f"Please run `generate_clusters.py` and `generate_centrality.py` first.")
        st.stop()

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
                # Use AI to parse structured data
                cv_data = doc_parser.get_structured_data(cv_text, analytics_engine.all_skills)
                job_data = doc_parser.get_structured_data(job_description_text, analytics_engine.all_skills)

                if cv_data and job_data:
                    # Run the full analysis
                    analysis_results = cv_analyzer.analyze(cv_data, job_data)
                    
                    # --- DISPLAY RESULTS ---
                    st.markdown("---")
                    st.header("🚀 Candidate Evaluation Report")
                    
                    # Display the AI-generated narrative report
                    st.markdown(analysis_results['ai_report'])
                    
                    # Display the data-driven breakdown in an expander
                    with st.expander("Show Data-Driven Metrics and Details"):
                        st.subheader("Quantitative Scores")
                        metric1, metric2 = st.columns(2)
                        
                        metric1.metric(
                            label="Weighted Skill Match Score", 
                            value=f"{analysis_results['weighted_score']:.1f}%", 
                            help="This score weights required skills by their market importance (centrality). A higher score means the candidate has the *most critical* skills for the role."
                        )
                        metric2.metric(
                            label="Domain Fit Score", 
                            value=f"{analysis_results['domain_fit_score']:.1f}%", 
                            help=f"This measures how much of the candidate's total skillset aligns with the job's primary domain, which we've identified as: {analysis_results['domain_name']}."
                        )

                        st.markdown("---")
                        
                        # Skill Breakdown
                        st.subheader("Skill Breakdown")
                        res_col1, res_col2 = st.columns(2)
                        
                        with res_col1:
                            st.success(f"✅ Matched Skills ({len(analysis_results['matched_skills'])}):")
                            st.write(f"`{', '.join(analysis_results['matched_skills'])}`" if analysis_results['matched_skills'] else "_None_")
                        
                        with res_col2:
                             st.error(f"❌ Missing Skills ({len(analysis_results['missing_skills'])}):")
                             st.write(f"`{', '.join(analysis_results['missing_skills'])}`" if analysis_results['missing_skills'] else "_None_")

                        st.info("💡 Potential Skills (Learnability Assessment)")
                        if not analysis_results['potential_skills']:
                            st.write("No strong potential skills found for the missing requirements.")
                        else:
                            for skill, info in analysis_results['potential_skills'].items():
                                st.write(f"- **{skill.title()}**: Can likely be learned quickly. This is inferred from their expertise in `{info['proxy'].title()}`. Learnability: **{info['learnability']}**.")

                else:
                    st.error("AI parsing failed. This can happen due to API issues or if the documents are empty/unreadable. Please check the content or try again.")
    else:
        st.warning("Please upload a CV and paste a job description to analyze.")