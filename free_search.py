import requests
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS
from typing import List, Dict

class FreeSearch:
    def __init__(self):
        self.ddgs = DDGS()

    def search(self, query: str, max_results: int = 8) -> List[Dict]:
        """
        Executes a DuckDuckGo web search.
        """
        results = []
        try:
            # Using text search
            search_results = self.ddgs.text(query, max_results=max_results)
            if not search_results:
                return results
                
            for res in search_results:
                results.append({
                    "title": res.get("title", ""),
                    "url": res.get("href", ""),
                    "snippet": res.get("body", "")
                })
        except Exception as e:
            print(f"Error during DuckDuckGo search: {e}")
            
        return results

    def fetch_url_content(self, url: str) -> str:
        """
        Optionally fetch more content from a URL using BeautifulSoup.
        """
        try:
            response = requests.get(url, timeout=5, headers={'User-Agent': 'Mozilla/5.0'})
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            # Extract basic text
            text = ' '.join([p.text for p in soup.find_all('p')])
            return text[:1000] # Limiting size
        except Exception:
            return ""
