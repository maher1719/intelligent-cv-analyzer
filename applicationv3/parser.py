# parser.py
import google.generativeai as genai
import streamlit as st
import json

class DocumentParser:
    def __init__(self, api_key):
        self.model = self._initialize_model(api_key)

    def _initialize_model(self, api_key):
        """Initializes and returns the Gemini model."""
        try:
            genai.configure(api_key=api_key)
            return genai.GenerativeModel('gemini-2.5-flash')
        except Exception as e:
            st.error(f"Error initializing Gemini API. Please check your API key. Details: {e}")
            return None
    
    def get_structured_data(self, text_content, all_known_skills):
        """Uses the Gemini model to parse text and extract structured information."""
        if not self.model:
            st.error("Gemini model is not initialized.")
            return None

        # Provide a sample of skills to guide the LLM
        skills_example_str = ", ".join(all_known_skills[:500])

        prompt = f"""
        Analyze the document text provided below. Your task is to extract the following information and return it ONLY as a valid JSON object. Do not include any other text or markdown formatting.

        1.  "technical_skills": A list of all technical skills mentioned. These skills must be from the provided master list.
        2.  "soft_skills": A list of soft skills mentioned (e.g., communication, teamwork, leadership).
        3.  "years_of_experience": An integer representing the total years of professional experience mentioned. If a range is given, take the average. If not mentioned, return 0.
        4.  "summary": A concise 2-sentence summary of the person's professional profile or the job's core responsibilities.

        Master Skill List (use for "technical_skills" only):
        [{skills_example_str}]

        Document Text:
        ---
        {text_content}
        ---

        JSON Output:
        """
        
        # --- START OF CORRECTION ---
        response = None # Initialize response to None before the try block
        try:
            response = self.model.generate_content(prompt)
            # Clean up potential markdown formatting from the response
            clean_response = response.text.replace('```json', '').replace('```', '').strip()
            parsed_json = json.loads(clean_response)
            
            # Validate and clean the skills list one more time
            if 'technical_skills' in parsed_json:
                # Ensure we have a list of strings from the model's output
                skills_from_ai = parsed_json['technical_skills']
                if not isinstance(skills_from_ai, list):
                    skills_from_ai = [] # Default to empty list if format is wrong

                validated_skills = [
                    str(skill).strip().lower() for skill in skills_from_ai 
                    if str(skill).strip().lower() in all_known_skills
                ]
                parsed_json['technical_skills'] = sorted(list(set(validated_skills)))
            
            return parsed_json

        except Exception as e:
            # Now we can safely check if response exists before trying to access it
            response_text = response.text if response else "No response received from API."
            st.error(f"An error occurred while communicating with or parsing the AI's response. Details: {e}")
            st.expander("Show AI Response that caused error:").code(response_text)
            return None
        # --- END OF CORRECTION ---