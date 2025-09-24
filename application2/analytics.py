# analytics.py
import pandas as pd
import streamlit as st

class SkillAnalytics:
    """
    An engine that holds and analyzes pre-computed skill data.
    It is initialized with already-loaded pandas DataFrames.
    """
    def __init__(self, co_occurrence_matrix, skill_clusters, centrality_scores):
        """
        Initializes the analytics engine with pre-loaded data.
        
        Args:
            co_occurrence_matrix (pd.DataFrame): DataFrame of skill correlations.
            skill_clusters (pd.DataFrame): DataFrame mapping skills to cluster IDs.
            centrality_scores (pd.DataFrame): DataFrame with centrality metrics for each skill.
        """
        self.matrix = co_occurrence_matrix
        self.clusters = skill_clusters
        self.centrality = centrality_scores
        
        # Extract the master skill list from the loaded matrix
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
                # Ensure skill names are in the matrix to prevent KeyErrors
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
        # Check if centrality data is available
        if self.centrality is None or 'Betweenness Centrality' not in self.centrality.columns:
            return []
            
        # Define a "bridge" skill as one in the top 10% of betweenness centrality
        bridge_threshold = self.centrality['Betweenness Centrality'].quantile(0.90)
        transferable = [
            skill for skill in owned_skills 
            if skill in self.centrality.index and self.centrality.loc[skill, 'Betweenness Centrality'] > bridge_threshold
        ]
        return sorted(transferable)