import os
import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from typing import Optional, Dict

class VectorCache:
    def __init__(self, cache_dir: str = "cache"):
        self.cache_dir = cache_dir
        os.makedirs(self.cache_dir, exist_ok=True)
        
        # Load lightweight fast embedding model
        self.model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        self.dim = self.model.get_sentence_embedding_dimension()
        
        self.index_path = os.path.join(self.cache_dir, "faiss.index")
        self.db_path = os.path.join(self.cache_dir, "db.json")
        
        if os.path.exists(self.index_path):
            self.index = faiss.read_index(self.index_path)
            with open(self.db_path, "r", encoding="utf-8") as f:
                self.db = json.load(f)
        else:
            self.index = faiss.IndexFlatL2(self.dim)
            self.db = []
            
    def get_similar(self, query: str, threshold: float = 0.5) -> Optional[Dict]:
        """
        Check if query already exists in cache (semantic search).
        threshold is L2 distance. Lower is more similar.
        """
        if self.index.ntotal == 0:
            return None
            
        q_emb = self.model.encode([query])
        distances, indices = self.index.search(q_emb, 1)
        
        best_dist = distances[0][0]
        best_idx = indices[0][0]
        
        if best_idx >= 0 and best_dist < threshold:
            print(f"Cache hit! Score: {best_dist}")
            return self.db[best_idx]
            
        return None
        
    def add(self, query: str, result_dict: dict):
        q_emb = self.model.encode([query])
        self.index.add(q_emb)
        self.db.append(result_dict)
        
        # Save to disk
        faiss.write_index(self.index, self.index_path)
        with open(self.db_path, "w", encoding="utf-8") as f:
            json.dump(self.db, f, indent=2)
