# analytics.py
import pandas as pd
import streamlit as st
from collections import Counter

class SkillAnalytics:
    """
    An engine that holds and analyzes pre-computed skill data.
    It is initialized with already-loaded pandas DataFrames.
    """
    def __init__(self, co_occurrence_matrix, skill_clusters, centrality_scores, skill_knowledge_base):
        """
        Initializes the analytics engine with pre-loaded data.
        """
        self.matrix = co_occurrence_matrix
        self.clusters = skill_clusters
        self.centrality = centrality_scores
        self.knowledge_base = skill_knowledge_base # Renamed for clarity
        
        if self.matrix is not None:
            self.all_skills = self.matrix.index.tolist()
        else:
            self.all_skills = []

    def find_potential_skills(self, owned_skills, missing_skills, threshold=0.3):
        """Finds skills the candidate can likely learn based on co-occurrence data."""
        potential_skills = {}
        for missing in missing_skills:
            best_proxy = None
            max_score = 0
            for owned in owned_skills:
                if missing in self.matrix.index and owned in self.matrix.columns:
                    score = self.matrix.loc[missing, owned]
                    if score > max_score:
                        max_score = score
                        best_proxy = owned
            
            if max_score > threshold:
                potential_skills[missing] = {'proxy': best_proxy, 'score': max_score}
        return potential_skills

    def find_transferable_skills(self, owned_skills):
        """Identifies highly versatile 'bridge' skills from the candidate's skill set."""
        if self.centrality is None or 'betweenness centrality' not in self.centrality.columns:
            return []
            
        bridge_threshold = self.centrality['betweenness centrality'].quantile(0.90)
        transferable = [
            skill for skill in owned_skills 
            if skill in self.centrality.index and self.centrality.loc[skill, 'betweenness centrality'] > bridge_threshold
        ]
        return sorted(transferable)
    
    def calculate_weighted_score(self, candidate_skills, job_skills):
        """Calculates a match score weighted by skill importance (Degree Centrality)."""
        candidate_set = set(candidate_skills)
        job_set = set(job_skills)
        job_skills_with_scores = {s for s in job_set if s in self.centrality.index}
        
        if not job_skills_with_scores: return 0.0

        total_possible_score = self.centrality.loc[list(job_skills_with_scores)]['degree centrality'].sum()
        
        matched_skills = candidate_set.intersection(job_skills_with_scores)
        if not matched_skills: return 0.0
            
        candidate_score = self.centrality.loc[list(matched_skills)]['degree centrality'].sum()
        
        return (candidate_score / total_possible_score) * 100 if total_possible_score > 0 else 0

    def calculate_domain_fit(self, candidate_skills, job_skills):
        """Calculates how well the candidate's skillset aligns with the job's primary domain using skill types."""
        # Use the knowledge_base which has the 'skill_type' column
        job_skill_ontology = self.knowledge_base[self.knowledge_base.index.isin(job_skills)]
        if job_skill_ontology.empty:
            return 0.0, "N/A", "Could not determine the primary domain for this job."

        # Find the most common skill_type in the job description
        primary_domain = job_skill_ontology['skill_type'].mode()[0]
        
        candidate_skill_ontology = self.knowledge_base[self.knowledge_base.index.isin(candidate_skills)]
        if candidate_skill_ontology.empty:
            return 0.0, primary_domain, "Candidate has no skills in the required domain."
            
        candidate_skills_in_domain = candidate_skill_ontology[candidate_skill_ontology['skill_type'] == primary_domain]
        
        fit_percentage = (len(candidate_skills_in_domain) / len(candidate_skills)) * 100 if candidate_skills else 0
        
        domain_representation = ", ".join(job_skill_ontology.head(3).index.str.title())
        
        justification = (f"The job's primary domain appears to be **{primary_domain}** (e.g., {domain_representation}). "
                         f"{len(candidate_skills_in_domain)} of the candidate's {len(candidate_skills)} skills fall within this domain.")
        
        return fit_percentage, primary_domain, justification

    def refine_potential_skills(self, potential_skills_dict):
        """Adds 'learnability' context using clusters and the knowledge base."""
        refined_potential = {}

        for missing, data in potential_skills_dict.items():
            proxy = data['proxy']
            learnability = "Medium (Related via usage patterns)" # Default
            try:
                # Check 1: Are they in the same skill cluster?
                if self.clusters.loc[missing, 'cluster_id'] == self.clusters.loc[proxy, 'cluster_id']:
                    learnability = "High (Within the same skill cluster)"
                
                # Check 2 (More specific): Do they share a Parent_Skill from the knowledge base?
                missing_parent = self.knowledge_base.loc[missing, 'parent_skill']
                proxy_parent = self.knowledge_base.loc[proxy, 'parent_skill']
                if pd.notna(missing_parent) and missing_parent != 'none' and missing_parent == proxy_parent:
                    learnability = f"Very High (Both are '{str(missing_parent).title()}' skills)"

            except KeyError:
                learnability = "Unknown"
            
            refined_potential[missing] = {**data, 'learnability': learnability}
        
        return refined_potential