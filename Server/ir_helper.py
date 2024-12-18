import os
from typing import List, Dict, Tuple
from werkzeug.utils import secure_filename

class InformationRetrievalModels:
    def __init__(self, documents: List[Tuple[str, str]] = None):
        """
        Initialize the Information Retrieval Models class.
        """
        self.documents = documents or []
        self.queries = []
        self.relevance_judgments = {}
    
    def create_relevance_judgments(self, queries: List[str]) -> Dict[str, Dict[int, float]]:
        """
        Create advanced relevance judgments for given queries.
        """
        self.queries = queries
        self.relevance_judgments = {}
        
        for query in queries:
            query_relevance = {}
            query_terms = set(query.lower().split())
            
            for doc_idx, (title, content) in enumerate(self.documents):
                doc_terms = set(content.lower().split())
                overlap_score = len(query_terms.intersection(doc_terms))
                query_relevance[doc_idx] = overlap_score
            
            self.relevance_judgments[query] = query_relevance
        
        return self.relevance_judgments
    
    def interference_model(self, query: str) -> List[Tuple[int, float]]:
        """
        Compute document relevance using an Interference Model approach.
        """
        if not self.documents or not query:
            return []
        
        relevance_scores = []
        query_terms = set(query.lower().split())
        
        for doc_idx, (title, content) in enumerate(self.documents):
            doc_terms = set(content.lower().split())
            overlap_score = len(query_terms.intersection(doc_terms))
            relevance_scores.append((doc_idx, overlap_score))
        
        return sorted(relevance_scores, key=lambda x: x[1], reverse=True)

    def belief_network(self, query: str) -> List[Tuple[int, float]]:
        """
        Enhanced Belief Network for document ranking.
        """
        if not self.documents or not query:
            return []
        
        relevance_scores = []
        query_terms = set(query.lower().split())
        
        for doc_idx, (title, content) in enumerate(self.documents):
            doc_terms = set(content.lower().split())
            overlap_score = len(query_terms.intersection(doc_terms))
            relevance_scores.append((doc_idx, overlap_score))
        
        return sorted(relevance_scores, key=lambda x: x[1], reverse=True)