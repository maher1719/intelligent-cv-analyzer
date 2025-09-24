import streamlit as st
import pandas as pd
import os
import warnings
import json
import google.generativeai as genai
from PyPDF2 import PdfReader
import docx2txt

# Suppress common warnings to keep the output clean
warnings.filterwarnings('ignore')

# --- CONFIGURATION ---
# These filenames must match the files you've already created.
CO_OCCURRENCE_FILE = 'skill_co_occurrence_matrix.csv'
CLUSTERS_FILE = 'skill_clusters.csv'
CENTRALITY_FILE = 'centrality_measures.csv'

# This threshold determines how related a skill must be to be considered a "potential" skill.
# 0.3 means a 30% correlation in your data. You can adjust this.
POTENTIAL_THRESHOLD = 0.3  

# --- DATA LOADING ---
@st.cache_data
def load_data():
    """Loads and prepares all the analysis data from your CSV files."""
    try:
        # Load the main co-occurrence matrix. The first column is the index.
        co_occurrence_matrix = pd.read_csv(CO_OCCURRENCE_FILE, index_col=0)
        
        # Load skill clusters and centrality scores, setting the 'Skill' column as the index for fast lookups.
        skill_clusters = pd.read_csv(CLUSTERS_FILE, index_col='Skill')
        centrality_scores = pd.read_csv(CENTRALITY_FILE, index_col='Skill')
        
        # Standardize all skill names to lowercase for consistent matching
        co_occurrence_matrix.index = co_occurrence_matrix.index.str.lower()
        co_occurrence_matrix.columns = co_occurrence_matrix.columns.str.lower()
        skill_clusters.index = skill_clusters.index.str.lower()
        centrality_scores.index = centrality_scores.index.str.lower()
        
        all_known_skills = co_occurrence_matrix.index.tolist()
        
        return co_occurrence_matrix, skill_clusters, centrality_scores, all_known_skills
        
    except FileNotFoundError as e:
        st.error(f"FATAL ERROR: Could not find a required data file: {e.filename}")
        st.error("Please make sure all your CSV files are in the same folder as this script.")
        return None, None, None, None

# --- LLM & ANALYSIS FUNCTIONS ---

def get_gemini_model(api_key):
    """Initializes the Gemini model with the provided API key."""
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        return model
    except Exception as e:
        st.error(f"Error initializing Gemini API. Please check your API key. Details: {e}")
        return None

def extract_skills_with_llm(model, text_content, all_known_skills):
    """Uses the Gemini model to extract skills from text, guided by our known skills list."""
    # We provide a large sample of our skills to guide the LLM
    skills_example_str = ", ".join(all_known_skills[:700]) # Use a substantial chunk of skills as a guide

    prompt = f"""
    Analyze the following text. Your task is to identify and extract all professional skills mentioned in it.
    Only extract skills that are present in this master list:
    Master Skill List: [{skills_example_str}]

    Text to Analyze:
    ---
    {text_content}
    ---
    
    Instructions:
    1. Read the "Text to Analyze" carefully.
    2. Compare the words and phrases in the text to the "Master Skill List".
    3. Return ONLY a comma-separated list of the skills you found.
    4. Do not add any explanation, headings, or introductory text.
    
    Example Output: python, javascript, react, aws, project management, data analysis
    """
    
    try:
        response = model.generate_content(prompt)
        # Clean up the LLM's output
        extracted_text = response.text.strip()
        skills = [skill.strip().lower() for skill in extracted_text.split(',')]
        # Final validation to ensure every returned skill is genuinely in our master list
        validated_skills = [s for s in skills if s in all_known_skills]
        return sorted(list(set(validated_skills)))
    except Exception as e:
        st.error(f"An error occurred while communicating with the Gemini API: {e}")
        return []

def analyze_skills(candidate_skills, job_skills, matrix, centrality):
    """Performs the main analysis and returns a dictionary of results."""
    candidate_set = set(candidate_skills)
    job_set = set(job_skills)

    matched_skills = sorted(list(candidate_set.intersection(job_set)))
    missing_skills = sorted(list(job_set.difference(candidate_set)))

    potential_skills = {}
    for missing in missing_skills:
        best_proxy = None
        max_score = 0
        for owned in candidate_set:
            if missing in matrix.index and owned in matrix.columns:
                score = matrix.loc[missing, owned]
                if score > max_score:
                    max_score = score
                    best_proxy = owned
        
        if max_score > POTENTIAL_THRESHOLD:
            potential_skills[missing] = {'proxy': best_proxy, 'score': max_score}

    # Define a "bridge" skill as one in the top 10% of betweenness centrality
    bridge_threshold = centrality['Betweenness Centrality'].quantile(0.90)
    transferable_skills = [
        skill for skill in candidate_set 
        if skill in centrality.index and centrality.loc[skill, 'Betweenness Centrality'] > bridge_threshold
    ]

    return {
        "matched": matched_skills,
        "missing": missing_skills,
        "potential": potential_skills,
        "transferable": sorted(transferable_skills)
    }

# --- STREAMLIT USER INTERFACE ---

st.set_page_config(layout="wide", page_title="CV Potential Seeker")
st.title("👨‍💻 CV Potential Seeker")
st.markdown("This tool analyzes a CV against a job description to uncover hidden potential and transferable skills using your custom data model and Google's Gemini AI for text understanding.")

# --- SIDEBAR FOR API KEY ---
st.sidebar.title("Configuration")
st.sidebar.markdown("To use this app, you need a Google AI API Key.")
api_key = st.sidebar.text_input("Enter your Google Gemini API Key", type="password")
st.sidebar.markdown("[Get your free API key from Google AI Studio](https://aistudio.google.com/app/apikey)")

# Load data
co_occurrence_matrix, skill_clusters, centrality_scores, all_known_skills = load_data()

# Initialize the Gemini model
model = None
if api_key:
    model = get_gemini_model(api_key)

# Main layout
if all_known_skills is not None:
    col1, col2 = st.columns(2)

    with col1:
        st.header("1. Upload Candidate's CV")
        uploaded_file = st.file_uploader("Upload a PDF or DOCX file", type=['pdf', 'docx'], label_visibility="collapsed")

    with col2:
        st.header("2. Paste Job Description")
        job_description_text = st.text_area("Paste the full job description here", height=250, label_visibility="collapsed", placeholder="e.g., We are looking for a Python developer with experience in Django, REST APIs, and Docker...")

    if st.button("Analyze Now", type="primary", use_container_width=True, disabled=(not model)):
        if not model:
            st.error("Please enter your Google Gemini API Key in the sidebar to enable analysis.")
        elif uploaded_file and job_description_text:
            with st.spinner("AI is reading and analyzing... This may take a moment."):
                
                # --- EXTRACT TEXT FROM UPLOADED FILE ---
                cv_text_content = ""
                try:
                    if uploaded_file.name.endswith('.pdf'):
                        pdf_reader = PdfReader(uploaded_file)
                        cv_text_content = "".join(page.extract_text() for page in pdf_reader.pages)
                    elif uploaded_file.name.endswith('.docx'):
                        cv_text_content = docx2txt.process(uploaded_file)
                except Exception as e:
                    st.error(f"Error reading file: {e}")
                    cv_text_content = None

                if cv_text_content:
                    # --- PROCESSING with LLM ---
                    cv_skills = extract_skills_with_llm(model, cv_text_content, all_known_skills)
                    job_req_skills = extract_skills_with_llm(model, job_description_text, all_known_skills)
                    
                    if not cv_skills:
                        st.error("The AI could not extract any relevant skills from the CV. The CV might be an image-based PDF or have an unusual format.")
                    elif not job_req_skills:
                        st.warning("The AI could not identify any relevant skills in the job description. The analysis may not be meaningful.")
                    else:
                        # --- ANALYSIS with your custom data ---
                        results = analyze_skills(cv_skills, job_req_skills, co_occurrence_matrix, centrality_scores)
                        
                        # --- DISPLAY RESULTS ---
                        st.markdown("---")
                        st.subheader("Analysis Results")
                        
                        match_count = len(results['matched'])
                        job_skill_count = len(job_req_skills)
                        match_percentage = (match_count / job_skill_count) * 100 if job_skill_count > 0 else 0
                        potential_count = len(results['potential'])
                        potential_percentage = ((match_count + potential_count) / job_skill_count) * 100 if job_skill_count > 0 else 0

                        metric1, metric2 = st.columns(2)
                        metric1.metric(label="Direct Skill Match", value=f"{match_percentage:.1f}%", help=f"Candidate has {match_count} of the {job_skill_count} required skills.")
                        metric2.metric(label="Potential Match Score", value=f"{potential_percentage:.1f}%", help="Score including skills the candidate can likely learn quickly based on their profile.")
                        
                        st.markdown("---")
                        res_col1, res_col2 = st.columns(2)

                        with res_col1:
                            st.success(f"✅ Matched Skills ({len(results['matched'])})")
                            st.markdown(f"**{', '.join(results['matched'])}**" if results['matched'] else "None")
                            
                            st.info(f"💡 Potential Skills ({potential_count})")
                            st.markdown("_These are required skills the candidate can likely learn quickly based on their existing skillset._")
                            if not results['potential']:
                                st.write("No strong potential skills found.")
                            else:
                                for skill, info in results['potential'].items():
                                    st.write(f"- **{skill.title()}** is missing, but is highly related to their skill in **`{info['proxy'].title()}`**.")
                        
                        with res_col2:
                            st.error(f"❌ Missing Skills ({len(results['missing'])})")
                            st.markdown(f"**{', '.join(results['missing'])}**" if results['missing'] else "None")
                            
                            st.warning(f"🌐 Key Transferable Skills ({len(results['transferable'])})")
                            st.markdown("_These are highly versatile skills that connect different knowledge domains, making the candidate a valuable team member._")
                            st.markdown(f"**{', '.join(results['transferable'])}**" if results['transferable'] else "No key transferable skills were identified.")

                        with st.expander("See Raw Skills Extracted by AI"):
                            st.json({
                                "Skills Found in CV": cv_skills,
                                "Skills Required by Job": job_req_skills
                            })
        else:
            st.warning("Please upload a CV and paste a job description to analyze.")
else:
    st.error("Application cannot start because data files are missing.")