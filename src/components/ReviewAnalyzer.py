import pandas as pd
import numpy as np
import re
from io import StringIO
import random
import string

class ReviewAnalyzer:
    """
    A class for analyzing product reviews to determine authenticity.
    
    In a real implementation, this would use NLP models like BERT or
    other machine learning algorithms trained on labeled fake/real reviews.
    """
    
    def __init__(self):
        """
        Initialize the ReviewAnalyzer.
        
        In a real implementation, this would load ML models and NLP resources.
        """
        # Placeholder for demonstration - in a real implementation these would be ML models
        self.fake_patterns = [
            r'!!+',  # Multiple exclamation marks
            r'best .{0,20}ever',  # Hyperbolic praise
            r'amazing .{0,20}perfect',  # Unrealistic praise
            r'life.?changing',  # Hyperbolic impact
            r'in exchange for .{0,40}review',  # Incentivized review disclosure
            r'received .{0,20}free',  # Free product
        ]
        self.compiled_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in self.fake_patterns]
    
    def analyze_reviews(self, reviews, threshold=0.7):
        """
        Analyze a list of reviews to determine authenticity.
        
        Args:
            reviews (list): List of review dictionaries.
            threshold (float): Confidence threshold for fake detection.
            
        Returns:
            dict: Results of the analysis including:
                - real_percentage: Percentage of reviews considered authentic
                - fake_percentage: Percentage of reviews considered fake
                - reviews: Detailed information on each review
                - export_csv: CSV string of detailed results
        """
        # In a real implementation, this would use ML models for prediction
        analyzed_reviews = []
        fake_count = 0
        
        for review in reviews:
            # Calculate a fake probability score in a real implementation
            # This would be done with NLP models
            fake_score = self._calculate_fake_probability(review)
            is_fake = fake_score > threshold
            
            if is_fake:
                fake_count += 1
                
            analyzed_reviews.append({
                "text": review["text"],
                "rating": review["rating"],
                "date": review["date"],
                "verified_purchase": review["verified_purchase"],
                "helpful_votes": review["helpful_votes"],
                "reviewer": review["reviewer"],
                "authenticity_score": 1 - fake_score,
                "is_fake": is_fake,
                "flags": self._get_flags(review, fake_score)
            })
        
        # Calculate percentages
        total = len(reviews)
        fake_percentage = round((fake_count / total) * 100) if total > 0 else 0
        real_percentage = 100 - fake_percentage
        
        # Create CSV for export
        csv_data = self._create_export_csv(analyzed_reviews)
        
        return {
            "real_percentage": real_percentage,
            "fake_percentage": fake_percentage,
            "reviews": analyzed_reviews,
            "export_csv": csv_data
        }
    
    def _calculate_fake_probability(self, review):
        """
        Calculate probability that a review is fake.
        
        In a real implementation, this would use NLP models.
        For demonstration, we use simple heuristics.
        
        Args:
            review (dict): Review data
            
        Returns:
            float: Probability between 0 and 1 that the review is fake
        """
        # Check for suspicious patterns in text
        text = review["text"].lower()
        pattern_matches = sum(1 for pattern in self.compiled_patterns if pattern.search(text))
        
        # Calculate base score from suspicious patterns
        pattern_score = min(0.7, pattern_matches * 0.15)
        
        # Adjust based on other factors
        adjustments = 0
        
        # Few helpful votes may indicate fake
        if review["helpful_votes"] == 0:
            adjustments += 0.05
            
        # Unverified purchases are more suspicious
        if not review["verified_purchase"]:
            adjustments += 0.15
            
        # New reviewers with few reviews are more suspicious
        if review["reviewer_history"]["total_reviews"] <= 2:
            adjustments += 0.1
            
        # Perfect 5-star ratings are more common in fake reviews
        if review["rating"] == 5:
            adjustments += 0.05
            
        # Very short reviews may be suspicious
        if len(text) < 20:
            adjustments += 0.1
            
        # Add randomness for demonstration purposes
        random_factor = random.uniform(-0.1, 0.1)
        
        # Combine factors
        final_score = min(0.95, max(0.05, pattern_score + adjustments + random_factor))
        
        return final_score
    
    def _get_flags(self, review, fake_score):
        """
        Generate flags explaining why a review might be fake.
        
        Args:
            review (dict): Review data
            fake_score (float): Calculated fake probability
            
        Returns:
            list: List of flag strings
        """
        flags = []
        text = review["text"].lower()
        
        # Check patterns
        for i, pattern in enumerate(self.compiled_patterns):
            if pattern.search(text):
                if i == 0:
                    flags.append("Excessive punctuation")
                elif i == 1:
                    flags.append("Hyperbolic language")
                elif i == 2:
                    flags.append("Unrealistic praise")
                elif i == 3:
                    flags.append("Exaggerated impact")
                elif i == 4 or i == 5:
                    flags.append("Incentivized review")
        
        # Check other factors
        if not review["verified_purchase"]:
            flags.append("Unverified purchase")
            
        if review["reviewer_history"]["total_reviews"] <= 2:
            flags.append("New reviewer")
            
        if review["helpful_votes"] == 0:
            flags.append("No helpful votes")
            
        if len(text) < 20:
            flags.append("Very short review")
            
        return flags
    
    def _create_export_csv(self, analyzed_reviews):
        """
        Create a CSV string from analyzed reviews.
        
        Args:
            analyzed_reviews (list): Analyzed review data
            
        Returns:
            str: CSV data as string
        """
        output = StringIO()
        
        # Create pandas DataFrame
        df = pd.DataFrame([{
            "Review Text": r["text"],
            "Rating": r["rating"],
            "Date": r["date"],
            "Verified Purchase": r["verified_purchase"],
            "Helpful Votes": r["helpful_votes"],
            "Reviewer": r["reviewer"],
            "Authenticity Score": f"{r['authenticity_score']:.2f}",
            "Is Fake": r["is_fake"],
            "Flags": ", ".join(r["flags"])
        } for r in analyzed_reviews])
        
        # Write to CSV
        df.to_csv(output, index=False)
        return output.getvalue()