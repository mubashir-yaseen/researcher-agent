import os
import json
import requests
from typing import Dict, Any
from .models import ResearchOutput, Source
from .free_search import FreeSearch
from .scorer import CredibilityScorer
from .vector_cache import VectorCache

class ResearcherAgent:
    def __init__(self):
        self.searcher = FreeSearch()
        self.cache = VectorCache()
        self.api_key = os.getenv("OPENROUTER_API_KEY", "")
        # DeepSeek setup via OpenRouter
        self.model = "deepseek/deepseek-coder" # Free tier OpenRouter Model, Llama 3.2 is also free depending on openrouter 'meta-llama/llama-3.2-11b-vision-instruct:free'

    def run(self, query: str) -> Dict[Any, Any]:
        """
        Execute full research workflow.
        """
        # 1. Check Cache
        cached = self.cache.get_similar(query)
        if cached:
            return cached
            
        # 2. Search
        raw_results = self.searcher.search(query, max_results=8)
        
        sources = []
        context_texts = []
        for r in raw_results:
            scores = CredibilityScorer.score_source(r['url'], r['snippet'])
            source_obj = Source(
                url=r['url'],
                title=r['title'],
                snippet=r['snippet'],
                credibility_score=scores['credibility_score'],
                recency_score=scores['recency_score']
            )
            sources.append(source_obj)
            context_texts.append(f"Title: {r['title']}\nSnippet: {r['snippet']}\nURL: {r['url']}")
            
        # 3. Call LLM for key facts via OpenRouter
        context_str = "\n\n".join(context_texts)
        system_prompt = (
            "You are a strict financial AI researcher. "
            "Analyze the provided search results and extract 3-5 concrete key facts relevant to the query. "
            "Return only valid JSON matching this schema: "
            "{\"key_facts\": [\"fact 1...\", ...], \"confidence\": 0.85, \"next_action\": \"send_to_verifier\"}. "
            "Respond ONLY with raw JSON. No markdown ticks like ```json"
        )
        user_prompt = f"Query: {query}\n\nSearch Results:\n{context_str}"
        
        llm_response = self._call_openrouter(system_prompt, user_prompt)
        
        # Parse LLM response
        try:
            parsed = json.loads(llm_response)
        except json.JSONDecodeError:
            # Fallback if LLM didn't return perfect JSON
            import re
            json_str = re.search(r'\{.*\}', llm_response, re.DOTALL)
            if json_str:
                parsed = json.loads(json_str.group(0))
            else:
                parsed = {
                    "key_facts": ["Failed to extract structured facts."],
                    "confidence": 0.0,
                    "next_action": "human_review"
                }
                
        # 4. Construct Final Output
        output = ResearchOutput(
            query=query,
            sources=sources,
            key_facts=parsed.get("key_facts", []),
            confidence=parsed.get("confidence", 0.0),
            next_action=parsed.get("next_action", "human_review")
        )
        
        final_dict = output.model_dump()
        
        # 5. Cache result
        self.cache.add(query, final_dict)
        
        return final_dict

    def _call_openrouter(self, system: str, user: str) -> str:
        if not self.api_key:
            return '{"key_facts": ["No OpenRouter API key provided."], "confidence": 0.0, "next_action": "add_api_key"}'
            
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": "http://localhost:8501", # Required by OpenRouter
            "X-Title": "Financial Researcher Agent",
        }
        
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user}
            ]
        }
        
        try:
            # Default openrouter chat completions endpoint
            response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"].strip()
        except Exception as e:
            print(f"LLM Error: {e}")
            return '{"key_facts": ["LLM API request failed."], "confidence": 0.0, "next_action": "retry"}'
