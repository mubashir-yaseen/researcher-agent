from urllib.parse import urlparse
import re
from datetime import datetime

DOMAINS = {
    'psx.com.pk': 0.95,
    'secp.gov.pk': 0.94,
    'dawn.com': 0.85,
    'tribune.com.pk': 0.82,
    'wsj.com': 0.85,
    'bloomberg.com': 0.88,
    'reuters.com': 0.88,
    'brecorder.com': 0.85, # Business Recorder Pakistan
    'bloomberg.com.pk': 0.85,
    'twitter.com': 0.40,
    'x.com': 0.40,
    'facebook.com': 0.30,
    'reddit.com': 0.40
}

class CredibilityScorer:
    @staticmethod
    def score_domain(url: str) -> float:
        try:
            domain = urlparse(url).netloc.lower()
            if domain.startswith("www."):
                domain = domain[4:]
            
            # Check exact match First
            if domain in DOMAINS:
                return DOMAINS[domain]
            
            # Check ends with (for subdomains)
            for k, v in DOMAINS.items():
                if domain.endswith(k):
                    return v
                    
            # Default fallback for unknown domains
            if domain.endswith('.gov') or domain.endswith('.gov.pk') or domain.endswith('.edu'):
                return 0.90
            
            return 0.60 # Baseline for neutral sites
        except Exception:
            return 0.50

    @staticmethod
    def score_recency(snippet: str) -> float:
        # Very basic mock recency scoring based on matching current year or recent dates 
        # In a real scenario, this would parse published_date from the webpage meta tags.
        current_year = str(datetime.now().year)
        if current_year in snippet:
            return 0.90
        
        # Look for things like "2 days ago", "Mar 15, 2026", etc.
        recent_patterns = [r'\b(today|yesterday|just now|hours ago)\b', r'\b\d{1,2}\s+(days|hours|minutes)\s+ago\b']
        for pattern in recent_patterns:
            if re.search(pattern, snippet, re.IGNORECASE):
                return 0.95
                
        return 0.70 # Default recency if no dates are obvious

    @classmethod
    def score_source(cls, url: str, snippet: str) -> dict:
        c_score = cls.score_domain(url)
        r_score = cls.score_recency(snippet)
        return {
            "credibility_score": c_score,
            "recency_score": r_score
        }
