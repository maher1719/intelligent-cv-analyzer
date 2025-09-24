# analyzer.py
import google.generativeai as genai
import pandas as pd

class CVAnalyzer:
    def __init__(self, ai_model, analytics_engine=None):
        """
        Initializes the analyzer.
        If analytics_engine is None, it runs in a data-less 'demo mode'.
        """
        self.model = ai_model
        self.analytics = analytics_engine
        self.is_demo_mode = analytics_engine is None

    def analyze(self, cv_data, job_data):
        """
        Orchestrates the analysis. Switches between full analysis and demo mode.
        """
        if self.is_demo_mode:
            return self._analyze_demo_mode(cv_data, job_data)
        else:
            return self._analyze_full_mode(cv_data, job_data)

    def _analyze_full_mode(self, cv_data, job_data):
        """Performs the comprehensive analysis using the local CSV knowledge base."""
        cv_skills = cv_data.get('technical_skills', [])
        job_skills = job_data.get('technical_skills', [])
        
        matched_skills = sorted(list(set(cv_skills).intersection(set(job_skills))))
        missing_skills = sorted(list(set(job_skills).difference(set(cv_skills))))
        
        # --- CORRECTED CALLS: Now calling methods on the analytics object ---
        potential_skills_raw = self.analytics.find_potential_skills(cv_skills, missing_skills)
        potential_skills = self.analytics.refine_potential_skills(potential_skills_raw)
        transferable = self.analytics.find_transferable_skills(cv_skills)
        weighted_score = self.analytics.calculate_weighted_score(cv_skills, job_skills)
        domain_fit_score, domain_name, domain_justification = self.analytics.calculate_domain_fit(cv_skills, job_skills)
        # --- END OF CORRECTIONS ---
        
        cv_exp = cv_data.get('years_of_experience', 0)
        job_exp = job_data.get('years_of_experience', 0)
        exp_match_text = "Meets or exceeds" if cv_exp >= job_exp else f"Below requirement ({cv_exp} years vs {job_exp} required)"

        analysis_data = {
            "cv_summary": cv_data.get('summary'),
            "job_summary": job_data.get('summary'),
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "potential_skills": potential_skills,
            "transferable_skills": transferable,
            "experience_match": exp_match_text,
            "weighted_score": weighted_score,
            "domain_fit_score": domain_fit_score,
            "domain_name": domain_name,
            "domain_justification": domain_justification
        }
        
        analysis_data['ai_report'] = self._generate_full_report(analysis_data)
        return analysis_data

    def _analyze_demo_mode(self, cv_data, job_data):
        """Performs a simplified analysis using only the LLM."""
        analysis_data = {
            "cv_summary": cv_data.get('summary'),
            "job_summary": job_data.get('summary'),
            "cv_skills": cv_data.get('technical_skills', []),
            "job_skills": job_data.get('technical_skills', []),
            "cv_experience": cv_data.get('years_of_experience', 0),
            "job_experience": job_data.get('years_of_experience', 0)
        }
        analysis_data['ai_report'] = self._generate_demo_report(analysis_data)
        return analysis_data
        
    def _generate_demo_report(self, data):
        """Generates a report using only LLM reasoning, without custom data."""
        prompt = f"""
        As an expert HR analyst, create a concise evaluation of a job candidate based ONLY on the information provided below. Do not invent scores or metrics.

        **CANDIDATE PROFILE:**
        - Experience: {data['cv_experience']} years
        - Skills: {', '.join(data['cv_skills']) or 'None'}
        - Summary: {data['cv_summary']}

        **JOB REQUIREMENTS:**
        - Experience: {data['job_experience']} years
        - Skills: {', '.join(data['job_skills']) or 'None'}
        - Summary: {data['job_summary']}

        **YOUR TASK:**
        Write a professional hiring assessment. Analyze the candidate's strengths and weaknesses for this specific role based on the skills and experience. Suggest potential areas where the candidate might need to upskill. Conclude with a general recommendation.
        """
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"An error occurred while generating the AI summary: {e}"
            
    def _generate_full_report(self, data):
        """Generates the full report using the rich, data-driven insights."""
        potential_str = "".join([f"- For '{s}', the candidate shows promise due to their experience with '{d['proxy']}'. Learnability is rated as: **{d['learnability']}**.\n" for s, d in data['potential_skills'].items()]) or "No strong related skills were found."

        prompt = f"""
        As an expert HR analyst, create a concise evaluation of a job candidate using the provided data-driven analysis.

        **CANDIDATE & JOB SUMMARY:**
        - Candidate: {data['cv_summary']}
        - Job: {data['job_summary']}

        **DATA-DRIVEN ANALYSIS:**
        - **Weighted Skill Score:** {data['weighted_score']:.1f}% (This score is weighted by the market importance of each required skill that the candidate possesses).
        - **Domain Fit Score:** {data['domain_fit_score']:.1f}% ({data['domain_justification']}).
        - **Experience Match:** {data['experience_match']}
        - **Directly Matched Skills:** {', '.join(data['matched_skills']) or 'None'}
        - **Missing Required Skills:** {', '.join(data['missing_skills']) or 'None'}
        - **Inferred Skill Potential & Learnability:**\n{potential_str}
        - **Key Transferable Skills:** {', '.join(data['transferable_skills']) or 'None'}

        **YOUR TASK:**
        Synthesize ALL of the above into a comprehensive report with the following markdown sections:

        ### Overall Assessment
        Write a 3-4 sentence paragraph summarizing the candidate's fit, integrating the **Weighted Skill Score** and **Domain Fit Score** to justify your conclusion. Provide a clear recommendation (e.g., "Strongly recommend for interview").

        ### Potential Fit & Time to Proficiency
        Provide a "Potential Fit" percentage score (e.g., 85%). Justify it using the direct matches, learnability of missing skills, and experience. Estimate the "Time to Full Proficiency" (e.g., "1-3 months").

        ### Strategic Value (Transferable Skills)
        Explain why the identified transferable skills are valuable for this specific role.
        """
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"An error occurred while generating the AI summary: {e}"