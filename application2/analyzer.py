# analyzer.py
import google.generativeai as genai
from collections import Counter

class CVAnalyzer:
    def __init__(self, analytics_engine, ai_model):
        self.analytics = analytics_engine
        self.model = ai_model

    def _calculate_weighted_score(self, candidate_skills, job_skills):
        """Calculates a match score weighted by skill importance (Degree Centrality)."""
        centrality_scores = self.analytics.centrality
        
        candidate_set = set(candidate_skills)
        job_set = set(job_skills)

        job_skills_with_scores = {s for s in job_set if s in centrality_scores.index}
        
        if not job_skills_with_scores:
            return 0.0

        total_possible_score = centrality_scores.loc[list(job_skills_with_scores)]['Degree Centrality'].sum()
        
        matched_skills = candidate_set.intersection(job_skills_with_scores)
        if not matched_skills:
            return 0.0
            
        candidate_score = centrality_scores.loc[list(matched_skills)]['Degree Centrality'].sum()
        
        return (candidate_score / total_possible_score) * 100 if total_possible_score > 0 else 0

    def _calculate_domain_fit(self, candidate_skills, job_skills):
        """Calculates how well the candidate's overall skillset aligns with the job's primary domain."""
        skill_clusters = self.analytics.clusters
        
        job_skill_clusters = skill_clusters.loc[skill_clusters.index.intersection(job_skills)]
        if job_skill_clusters.empty:
            return 0.0, "N/A"
            
        primary_cluster_id = job_skill_clusters['Cluster_ID'].mode()[0]
        
        candidate_skills_in_cluster = [
            s for s in candidate_skills 
            if s in skill_clusters.index and skill_clusters.loc[s, 'Cluster_ID'] == primary_cluster_id
        ]
        
        fit_percentage = (len(candidate_skills_in_cluster) / len(candidate_skills)) * 100 if candidate_skills else 0
        
        cluster_name_skills = job_skill_clusters[job_skill_clusters['Cluster_ID'] == primary_cluster_id].head(3).index.str.title()
        cluster_name = ", ".join(cluster_name_skills)
        
        return fit_percentage, f"Cluster {int(primary_cluster_id)} ({cluster_name})"

    def _refine_potential_skills(self, potential_skills_dict):
        """Adds 'learnability' context to potential skills based on clusters."""
        skill_clusters = self.analytics.clusters
        refined_potential = {}

        for missing, data in potential_skills_dict.items():
            proxy = data['proxy']
            try:
                missing_cluster = skill_clusters.loc[missing, 'Cluster_ID']
                proxy_cluster = skill_clusters.loc[proxy, 'Cluster_ID']
                
                if missing_cluster == proxy_cluster:
                    learnability = "High (within the same skill domain)"
                else:
                    learnability = "Medium (bridges related skill domains)"
                
                refined_potential[missing] = {**data, 'learnability': learnability}
            except KeyError:
                refined_potential[missing] = {**data, 'learnability': "Unknown"}
        
        return refined_potential
        
    def analyze(self, cv_data, job_data):
        """Performs a comprehensive analysis of the CV against the job description."""
        cv_skills = cv_data.get('technical_skills', [])
        job_skills = job_data.get('technical_skills', [])
        
        matched_skills = sorted(list(set(cv_skills).intersection(set(job_skills))))
        
        # --- THIS IS THE CORRECTED LINE ---
        missing_skills = sorted(list(set(job_skills).difference(set(cv_skills))))
        # ---------------------------------
        
        potential_skills_raw = self.analytics.find_potential_skills(cv_skills, missing_skills)
        potential_skills = self._refine_potential_skills(potential_skills_raw)
        transferable = self.analytics.find_transferable_skills(cv_skills)
        weighted_score = self._calculate_weighted_score(cv_skills, job_skills)
        domain_fit_score, domain_name = self._calculate_domain_fit(cv_skills, job_skills)
        
        cv_exp = cv_data.get('years_of_experience', 0)
        job_exp = job_data.get('years_of_experience', 0)
        exp_match = "Meets or exceeds" if cv_exp >= job_exp else f"Below requirement ({cv_exp} years vs {job_exp} required)"

        analysis_data = {
            "cv_summary": cv_data.get('summary'),
            "job_summary": job_data.get('summary'),
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "potential_skills": potential_skills,
            "transferable_skills": transferable,
            "experience_match": exp_match,
            "weighted_score": weighted_score,
            "domain_fit_score": domain_fit_score,
            "domain_name": domain_name
        }
        
        analysis_data['ai_report'] = self._generate_final_report(analysis_data)
        
        return analysis_data

    def _generate_final_report(self, analysis_data):
        """Asks the LLM to synthesize all findings into a final report."""
        if not self.model:
            return "AI Model not available for final report generation."

        matched_str = ", ".join(analysis_data['matched_skills']) or "None"
        missing_str = ", ".join(analysis_data['missing_skills']) or "None"
        transferable_str = ", ".join(analysis_data['transferable_skills']) or "None"
        
        potential_str = ""
        for skill, data in analysis_data['potential_skills'].items():
            potential_str += f"- For '{skill}', the candidate shows promise due to their experience with '{data['proxy']}'. Learnability is rated as: {data['learnability']}.\n"
        if not potential_str:
            potential_str = "No strong related skills were found for the missing requirements."

        prompt = f"""
        As an expert HR analyst, create a concise evaluation of a job candidate. You are given a summary of their CV, the job description, and a detailed, data-driven skill analysis.

        **CANDIDATE PROFILE SUMMARY:**
        {analysis_data['cv_summary']}

        **JOB DESCRIPTION SUMMARY:**
        {analysis_data['job_summary']}

        **DATA-DRIVEN ANALYSIS:**
        - **Weighted Skill Score:** {analysis_data['weighted_score']:.1f}% (This score is weighted by how important each skill is in the job market).
        - **Domain Fit Score:** {analysis_data['domain_fit_score']:.1f}% (This measures how much the candidate's overall skillset aligns with the job's primary skill domain, which is '{analysis_data['domain_name']}').
        - **Experience:** {analysis_data['experience_match']}
        - **Directly Matched Skills:** {matched_str}
        - **Missing Required Skills:** {missing_str}
        - **Inferred Skill Potential:**
        {potential_str}
        - **Key Transferable Skills Identified:** {transferable_str}

        **YOUR TASK:**
        Based on ALL of the information above, provide the following three sections in your response. Use markdown for formatting.
        Also based on CV skills how much current skills is transformable and also hidden connect skills in CV not only direct matching skills and keywords
        Also use project description and skills to gain more knowldge about the candidat CV and similarity of skills and hidden skills to job description
        Also generative skills like 'app application' or 'web application' is match if the CV have the component to meet the generative description
        ### Overall Assessment
        Write a 3-4 sentence paragraph summarizing the candidate's fit. Is this a strong candidate, a potential one that needs training, or a poor fit? Justify your conclusion using the provided scores and skill data.

        ### Potential Fit & Time to Proficiency
        Provide a "Potential Fit" percentage score (e.g., 85%). Justify this score by referencing the direct matches, the inferred skill potential, and their experience level. Then, estimate the "Time to Full Proficiency" (e.g., "1-2 months", "3-6 months") for this candidate to become fully productive in the role, considering the 'learnability' ratings.

        ### Transferable Skills Analysis
        Explain in a medium-length paragraph (3-5 sentences) why the identified transferable skills (if any) are valuable for this specific role. How does having skills like 'project management' or 'api design' make them a stronger, more well-rounded candidate for a role focused on '{analysis_data['job_summary']}'?
        """

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"An error occurred while generating the AI summary: {e}"