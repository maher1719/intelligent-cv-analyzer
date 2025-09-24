# analyzer.py
import google.generativeai as genai

class CVAnalyzer:
    def __init__(self, analytics_engine, ai_model):
        self.analytics = analytics_engine
        self.model = ai_model

    def analyze(self, cv_data, job_data):
        """Performs a comprehensive analysis of the CV against the job description."""
        cv_skills = set(cv_data.get('technical_skills', []))
        job_skills = set(job_data.get('technical_skills', []))

        matched_skills = sorted(list(cv_skills.intersection(job_skills)))
        # --- THIS IS THE CORRECTED LINE ---
        missing_skills = sorted(list(job_skills.difference(cv_skills)))
        # ---------------------------------
        
        potential = self.analytics.find_potential_skills(cv_skills, missing_skills)
        transferable = self.analytics.find_transferable_skills(cv_skills)
        
        # Experience comparison
        cv_exp = cv_data.get('years_of_experience', 0)
        job_exp = job_data.get('years_of_experience', 0)
        exp_match = "Meets or exceeds" if cv_exp >= job_exp else f"Below requirement ({cv_exp} vs {job_exp} years)"

        analysis_data = {
            "cv_summary": cv_data.get('summary'),
            "job_summary": job_data.get('summary'),
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "potential_skills": potential,
            "transferable_skills": transferable,
            "experience_match": exp_match
        }
        
        # Generate the final human-readable report using the AI
        analysis_data['ai_report'] = self._generate_final_report(analysis_data)
        
        return analysis_data

    def _generate_final_report(self, analysis_data):
        """Asks the LLM to synthesize all findings into a final report."""
        if not self.model:
            return "AI Model not available for final report generation."

        # Prepare the data for the prompt
        matched_str = ", ".join(analysis_data['matched_skills']) or "None"
        missing_str = ", ".join(analysis_data['missing_skills']) or "None"
        transferable_str = ", ".join(analysis_data['transferable_skills']) or "None"
        
        potential_str = ""
        for skill, data in analysis_data['potential_skills'].items():
            potential_str += f"- For '{skill}', the candidate shows promise due to their experience with the related skill '{data['proxy']}'.\n"
        if not potential_str:
            potential_str = "No strong related skills were found for the missing requirements."

        prompt = f"""
        As an expert HR analyst, CV evaluator , create a concise evaluation of a job candidate. You are given a summary of their CV, the job description, and a detailed, data-driven skill analysis.

        **CANDIDATE PROFILE SUMMARY:**
        {analysis_data['cv_summary']}

        **JOB DESCRIPTION SUMMARY:**
        {analysis_data['job_summary']}

        **DATA-DRIVEN ANALYSIS:**
        - **Experience:** {analysis_data['experience_match']}
        - **Directly Matched Skills:** {matched_str}
        - **Missing Required Skills:** {missing_str}
        - **Inferred Skill Potential:**
        {potential_str}
        - **Key Transferable Skills Identified:** {transferable_str}

        **YOUR TASK:**
        Based on all the information above, provide the following three sections in your response. Use markdown for formatting.

        ### Overall Assessment
        Write a 3-4 sentence paragraph summarizing the candidate's fit. Is this a strong candidate? A potential one that needs training? Or a poor fit? Justify your conclusion.

        ### Potential Fit & Time to Proficiency
        Provide a "Potential Fit" percentage score (e.g., 85%). Justify this score by referencing the direct matches, the potential for learning missing skills, and their experience level. Then, estimate the "Time to Full Proficiency" (e.g., "1-2 months", "3-6 months") for this candidate to become fully productive in the role.

        ### Transferable Skills Analysis
        Explain why the identified transferable skills (if any) are valuable for this specific role. How does having skills like 'project management' or 'data analysis' make them a stronger candidate, even if the role isn't explicitly for a project manager or data analyst?
        """

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"An error occurred while generating the AI summary: {e}"