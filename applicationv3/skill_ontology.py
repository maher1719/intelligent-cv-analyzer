import pandas as pd
import google.generativeai as genai
import time
import re
import os

# --- CONFIGURATION ---
# IMPORTANT: Put your Google AI API Key here
# You can get one from https://aistudio.google.com/app/apikey
API_KEY = "AIzaSyAD30hzssF3ozDEM1RFi97bVHJQNBMQSfY" 

# Input file to get the master list of skills from
# This should be your main co-occurrence matrix file
SKILLS_SOURCE_FILE = 'csv/correspendentFinalCleanTranspose.csv'

# The name of the new file we will create
OUTPUT_ONTOLOGY_FILE = 'skill_ontology.csv'

# How many skills to process in each API call.
# Keep this reasonably low to avoid overly long prompts.
BATCH_SIZE = 50

# --- SCRIPT LOGIC ---

def initialize_gemini():
    """Initializes the Gemini API and returns the model object."""
    try:
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel('gemini-2.5-flash')
        # Quick test to ensure the API key is valid
        model.generate_content("test", generation_config={"max_output_tokens": 10})
        print("Successfully connected to Google Gemini API.")
        return model
    except Exception as e:
        print(f"Error initializing Gemini API: {e}")
        print("Please check your API_KEY in the script.")
        return None

def generate_ontology_batch(model, skill_batch):
    """Sends a batch of skills to the Gemini API for categorization."""
    
    # Create a clean, comma-separated string of skills for the prompt
    skills_to_process = ", ".join([f'"{skill}"' for skill in skill_batch])

    prompt = f"""
    You are a technical skills classification expert. Your task is to categorize a list of professional skills.
    For each skill in the list below, determine its 'Skill_Type' and its 'Parent_Skill'.

    Here are the primary Skill_Type categories to use:
    - Programming Language
    - Framework/Library (for specific frameworks or libraries)
    - Database
    - Platform (e.g., AWS, Azure, Salesforce)
    - Tool (e.g., Git, Docker, Photoshop, Jira)
    - Protocol (e.g., HTTP, TCP/IP, API)
    - Methodology (e.g., Agile, Scrum, DevOps)
    - Soft Skill (e.g., Communication, Leadership, Teamwork)
    - Field (e.g., Data Science, Cybersecurity, Mechanical Engineering)
    - Other (for anything that doesn't fit)

    For 'Parent_Skill', identify the broader category or language it belongs to.
    - For 'React', the parent is 'javascript'.
    - For 'Django', the parent is 'python'.
    - For 'MySQL', the parent is 'sql'.
    - For a general language like 'Python', the parent can be 'programming language'.
    - For a soft skill like 'Leadership', the parent can be 'soft skill'.
    - If there is no clear parent, use 'none'.

    Analyze this list: {skills_to_process}

    Provide the output ONLY as a list of comma-separated values (CSV) with NO HEADER.
    Each line must follow this exact format: "Skill","Skill_Type","Parent_Skill"
    
    Example response for the skills "React", "Python", "Teamwork":
    "React","Framework/Library","javascript"
    "Python","Programming Language","programming language"
    "Teamwork","Soft Skill","soft skill"
    """

    try:
        response = model.generate_content(prompt,
                                          generation_config={"temperature": 0.1}) # Low temperature for consistent formatting
        return response.text
    except Exception as e:
        print(f"  -- API call failed for a batch. Error: {e}. Skipping this batch.")
        return ""

def main():
    if API_KEY == "YOUR_API_KEY_HERE":
        print("ERROR: Please update the API_KEY variable in the script with your Google Gemini API key.")
        return

    model = initialize_gemini()
    if not model:
        return

    print(f"Reading unique skills from '{SKILLS_SOURCE_FILE}'...")
    try:
        df_skills = pd.read_csv(SKILLS_SOURCE_FILE, index_col=0)
        # Use the index (which contains the skill names)
        all_skills = df_skills.index.unique().tolist()
        print(f"Found {len(all_skills)} unique skills to categorize.")
    except FileNotFoundError:
        print(f"ERROR: Cannot find the source file '{SKILLS_SOURCE_FILE}'.")
        return

    # Check if the output file already exists to allow resuming
    if os.path.exists(OUTPUT_ONTOLOGY_FILE):
        print(f"'{OUTPUT_ONTOLOGY_FILE}' already exists. Reading processed skills...")
        df_existing = pd.read_csv(OUTPUT_ONTOLOGY_FILE)
        processed_skills = set(df_existing['Skill'].str.lower())
        print(f"Found {len(processed_skills)} skills already processed. Resuming from where we left off.")
    else:
        processed_skills = set()
        # Create the file and write the header
        with open(OUTPUT_ONTOLOGY_FILE, 'w', newline='', encoding='utf-8') as f:
            f.write("Skill,Skill_Type,Parent_Skill\n")

    # Filter out skills that have already been processed
    skills_to_process = [s for s in all_skills if s.lower() not in processed_skills]
    
    if not skills_to_process:
        print("All skills have already been processed. Nothing to do.")
        return

    print(f"Starting categorization for {len(skills_to_process)} new skills...")

    with open(OUTPUT_ONTOLOGY_FILE, 'a', newline='', encoding='utf-8') as f:
        # Process the skills in batches
        for i in range(0, len(skills_to_process), BATCH_SIZE):
            batch = skills_to_process[i:i + BATCH_SIZE]
            print(f"Processing batch {i//BATCH_SIZE + 1} of {len(skills_to_process)//BATCH_SIZE + 1}...")
            
            # Call the Gemini API
            api_result = generate_ontology_batch(model, batch)
            
            # Clean and write the results to the file
            for line in api_result.strip().split('\n'):
                # Simple validation to ensure the line has three comma-separated values
                if line.count(',') == 2:
                    f.write(line + '\n')
            
            # Be respectful of API rate limits
            time.sleep(1.5) 

    print("\n--- Process Complete! ---")
    print(f"Skill ontology saved to '{OUTPUT_ONTOLOGY_FILE}'.")
    
    # Verify the output
    final_df = pd.read_csv(OUTPUT_ONTOLOGY_FILE)
    print("\nPreview of the created file:")
    print(final_df.head())
    print(f"\nTotal skills categorized: {len(final_df)}")


if __name__ == "__main__":
    main()