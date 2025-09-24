import streamlit as st
import pandas as pd
import os
import re
import warnings
import json

# Suppress common warnings to keep the output clean
warnings.filterwarnings('ignore')

# --- CONFIGURATION ---
CO_OCCURRENCE_FILE = 'skill_co_occurrence_matrix.csv' # Transposed version
CLUSTERS_FILE = 'skill_clusters.csv'
CENTRALITY_FILE = 'centrality_measures.csv'
POTENTIAL_THRESHOLD = 0.3  # Skills with correlation > 30% are considered potential matches

# --- DATA LOADING ---
@st.cache_data
def load_data():
    """Loads and prepares all the analysis data from your CSV files."""
    try:
        co_occurrence_matrix = pd.read_csv(CO_OCCURRENCE_FILE, index_col=0)
        skill_clusters = pd.read_csv(CLUSTERS_FILE, index_col='Skill')
        centrality_scores = pd.read_csv(CENTRALITY_FILE, index_col='Skill')
        
        # Convert all skill names to lowercase for consistent matching
        co_occurrence_matrix.index = co_occurrence_matrix.index.str.lower()
        co_occurrence_matrix.columns = co_occurrence_matrix.columns.str.lower()
        skill_clusters.index = skill_clusters.index.str.lower()
        centrality_scores.index = centrality_scores.index.str.lower()
        
        all_known_skills = co_occurrence_matrix.index.tolist()
        
        return co_occurrence_matrix, skill_clusters, centrality_scores, all_known_skills
    except FileNotFoundError as e:
        st.error(f"FATAL ERROR: Could not find a required data file: {e.filename}")
        st.error("Please make sure all CSV files are in the same folder as this script.")
        return None, None, None, None

# --- LLM INTEGRATION ---

# OPTION A: Local Gemma with Ollama
def get_llm_gemma():
    from langchain_community.llms import Ollama
    try:
        llm = Ollama(model="gemma:2b")
        # Test the connection
        llm.invoke("hello")
        return llm
    except Exception as e:
        st.error("Could not connect to Ollama. Is it running? You can start it by typing 'ollama serve' in your terminal.")
        return None

# OPTION B: Gemini API
def get_llm_gemini(api_key):
    import google.generativeai as genai
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
        return model
    except Exception as e:
        st.error(f"Error initializing Gemini API: {e}")
        return None

def extract_skills_with_llm(llm, text_content, all_known_skills, model_type='gemini'):
    """Uses an LLM to extract skills from text, guided by our known skills list."""
    # Convert list to a comma-separated string for the prompt
    skills_str = ", ".join(all_known_skills[:500]) # Limit to 500 to not overload the prompt

    prompt = f"""
    From the following text, please extract all skills that are present in this master list.
    Master Skill List: [{skills_str}]
    
    Text to analyze:
    ---
    {text_content}
    ---
    
    Return your answer as a clean, comma-separated list of the skills you found. For example: python, javascript, react, aws
    Do not include any other text, explanation, or formatting.
    """
    
    try:
        if model_type == 'gemini':
            response = llm.generate_content(prompt)
            extracted_text = response.text
        else: # Assumes LangChain model (Ollama)
            extracted_text = llm.invoke(prompt)
            
        # Clean the output
        skills = [skill.strip().lower() for skill in extracted_text.split(',')]
        # Final check to ensure skills are in our known list
        return sorted([s for s in skills if s in all_known_skills])
    except Exception as e:
        st.error(f"An error occurred while communicating with the LLM: {e}")
        return []


# --- ANALYSIS FUNCTIONS (No change needed here) ---
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

# --- STREAMLIT UI ---
st.set_page_config(layout="wide")
st.title("👨‍💻 CV Potential Seeker")
st.markdown("This tool analyzes a CV against a job description to uncover hidden potential and transferable skills using a data-driven model.")

# Load data first
co_occurrence_matrix, skill_clusters, centrality_scores, all_known_skills = load_data()

# Sidebar for configuration
st.sidebar.title("Configuration")
llm_option = st.sidebar.radio("Choose AI Model", ("Local Gemma (via Ollama)", "Google Gemini API"))
llm = None

if llm_option == "Local Gemma (via Ollama)":
    st.sidebar.info("Make sure the Ollama application is running on your computer.")
    llm = get_llm_gemma()
    model_type = 'ollama'
else:
    api_key = st.sidebar.text_input("Enter your Google AI API Key", type="password")
    if api_key:
        llm = get_llm_gemini(api_key)
        model_type = 'gemini'

# Main layout
if all_known_skills is not None:
    col1, col2 = st.columns(2)

    with col1:
        st.header("1. Upload Candidate's CV")
        uploaded_file = st.file_uploader("Upload a PDF or DOCX file", type=['pdf', 'docx'], label_visibility="collapsed")

    with col2:
        st.header("2. Paste Job Description")
        job_description_text = st.text_area("Paste the full job description here", height=250, label_visibility="collapsed")

    if st.button("Analyze Now", type="primary", use_container_width=True, disabled=(llm is None)):
        if llm is None:
            st.error("AI Model not configured. Please check your settings in the sidebar.")
        elif uploaded_file and job_description_text:
            with st.spinner("Reading CV and analyzing... This might take a moment."):
                # To use pyresparser, we need to save the file temporarily
                if not os.path.exists("temp"):
                    os.makedirs("temp")
                temp_file_path = os.path.join("temp", uploaded_file.name)
                with open(temp_file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())

                # --- Use a basic text extraction for the LLM ---
                # This part can be improved with better PDF-to-text libraries if needed
                if uploaded_file.name.endswith(".pdf"):
                    from PyPDF2 import PdfReader
                    reader = PdfReader(temp_file_path)
                    cv_text_content = "".join(page.extract_text() for page in reader.pages)
                else: # Assuming .docx
                    import docx2txt
                    cv_text_content = docx2txt.process(temp_file_path)
                
                # --- PROCESSING with LLM ---
                cv_skills = extract_skills_with_llm(llm, cv_text_content, all_known_skills, model_type)
                job_req_skills = extract_skills_with_llm(llm, job_description_text, all_known_skills, model_type)
                
                os.remove(temp_file_path) # Clean up

                if not cv_skills:
                    st.error("The AI could not extract any relevant skills from the CV. Please check the file's content.")
                elif not job_req_skills:
                    st.warning("The AI could not identify any relevant skills in the job description.")
                else:
                    # --- ANALYSIS with your custom data ---
                    results = analyze_skills(cv_skills, job_req_skills, co_occurrence_matrix, centrality_scores)
                    
                    # --- DISPLAY RESULTS ---
                    st.markdown("---")
                    st.subheader("Analysis Results")
                    
                    match_count = len(results['matched'])
                    job_skill_count = len(job_req_skills) if job_req_skills else 0
                    match_percentage = (match_count / job_skill_count) * 100 if job_skill_count > 0 else 0
                    potential_count = len(results['potential'])
                    potential_percentage = ((match_count + potential_count) / job_skill_count) * 100 if job_skill_count > 0 else 0

                    metric1, metric2 = st.columns(2)
                    metric1.metric(label="Direct Skill Match", value=f"{match_percentage:.1f}%", help=f"Candidate has {match_count} of the {job_skill_count} required skills.")
                    metric2.metric(label="Potential Match Score", value=f"{potential_percentage:.1f}%", help="Score including skills the candidate can likely learn quickly.")
                    
                    st.markdown("---")
                    res_col1, res_col2 = st.columns(2)

                    with res_col1:
                        st.success(f"✅ Matched Skills ({len(results['matched'])})")
                        st.markdown(f"**{', '.join(results['matched'])}**" if results['matched'] else "None")
                        
                        st.info(f"💡 Potential Skills ({potential_count})")
                        st.markdown("_These are required skills the candidate likely knows or can learn quickly based on their existing skillset._")
                        if not results['potential']:
                            st.write("No strong potential skills found.")
                        else:
                            for skill, info in results['potential'].items():
                                st.write(f"- **{skill.title()}**: Related to their knowledge of `{info['proxy'].title()}`")

                    with res_col2:
                        st.error(f"❌ Missing Skills ({len(results['missing'])})")
                        st.markdown(f"**{', '.join(results['missing'])}**" if results['missing'] else "None")
                        
                        st.warning(f"🌐 Key Transferable Skills ({len(results['transferable'])})")
                        st.markdown("_These are highly versatile skills that connect different knowledge domains._")
                        st.markdown(f"**{', '.join(results['transferable'])}**" if results['transferable'] else "No key transferable skills identified.")

                    with st.expander("Show Raw Skill Data Extracted by AI"):
                        st.json({
                            "Skills found in CV": cv_skills,
                            "Skills required by Job": job_req_skills
                        })
        else:
            st.warning("Please upload a CV and paste a job description to analyze.")
else:
    st.error("Could not load the necessary data files. The application cannot start.")