import numpy as np
import re
from typing import List, Set, Dict
from collections import defaultdict

class TextProcessor:
    """Handles text preprocessing and analysis."""
    
    @staticmethod
    def preprocess_text(text: str) -> List[str]:
        """Clean and tokenize text."""
        words = text.lower().split()
        words = [re.sub(r'[^a-zA-Z\s]', '', word) for word in words]
        return [word for word in words if word]

    @staticmethod
    def create_vocabulary(documents: List[str], stop_words: Set[str] = None) -> List[str]:
        """Create vocabulary from documents excluding stop words."""
        if stop_words is None:
            stop_words = set()
        vocabulary = set()
        for doc in documents:
            words = TextProcessor.preprocess_text(doc)
            vocabulary.update([word for word in words if word not in stop_words])
        return sorted(list(vocabulary))

    @staticmethod
    def create_binary_vector(text: str, vocabulary: List[str]) -> np.ndarray:
        """Create a binary vector for text based on vocabulary."""
        words = set(TextProcessor.preprocess_text(text))
        return np.array([1 if term in words else 0 for term in vocabulary])

    @staticmethod
    def calculate_jaccard_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Calculate Jaccard similarity between two binary vectors."""
        intersection = np.sum(vec1 & vec2)
        union = np.sum(vec1 | vec2)
        return intersection / union if union != 0 else 0

class DocumentSearcher:
    """Handles advanced document search operations."""

    @classmethod
    def binary_term_matching(cls, documents: List[dict], query: str):
        """Perform binary term matching search."""
        if not documents:
            return []

        # Create vocabulary and vectors
        documents_content = [doc['content'] for doc in documents]
        vocabulary = TextProcessor.create_vocabulary(documents_content + [query])
        print("Vocabulary")
        doc_vectors = np.array([
            TextProcessor.create_binary_vector(doc['content'], vocabulary)
            for doc in documents
        ])
        query_vector = TextProcessor.create_binary_vector(query, vocabulary)
        print("Binary Vectors Created")
        # Calculate similarities
        similarities = [
            TextProcessor.calculate_jaccard_similarity(doc_vec, query_vector)
            for doc_vec in doc_vectors
        ]
        print("Similarities Calculated")

        # Return sorted results with similarity and document
        results = [
            {
                'title': doc['title'], 
                'content': doc['content'], 
                'similarity': sim
            } 
            for doc, sim in zip(documents, similarities)
        ]
        print("Results")
        return sorted(results, key=lambda x: x['similarity'], reverse=True)

    @classmethod
    def non_overlapping_lists_search(cls, documents: List[dict], terms: List[str]):
        """
        Perform non-overlapping lists search.
        
        Args:
            documents (List[dict]): List of documents to search
            terms (List[str]): List of search terms
        
        Returns:
            List[dict]: List of non-overlapping documents
        """
        # Create a mapping of terms to documents
        term_to_docs = {}
        processed_docs = {}

        # Preprocess documents and create term-to-docs mapping
        for idx, doc in enumerate(documents):
            # Store processed document for later reference
            processed_docs[idx] = doc['content'].lower()
            
            # Check for each term
            for term in terms:
                term_lower = term.lower()
                if term_lower in processed_docs[idx]:
                    if term not in term_to_docs:
                        term_to_docs[term] = []
                    term_to_docs[term].append(idx)

        # Find non-overlapping documents
        non_overlapping_docs = set()
        for term, doc_list in term_to_docs.items():
            for doc_id in doc_list:
                # Ensure that the document is not already in the non-overlapping set
                if doc_id not in non_overlapping_docs:
                    # Check if this document contains only one term of interest
                    term_count = sum(1 for other_term in terms if other_term.lower() in processed_docs[doc_id])
                    if term_count == 1:  # Only add document if it contains exactly one term of interest
                        non_overlapping_docs.add(doc_id)

        # Convert document IDs to document details
        results = [
            {
                'title': documents[doc_id]['title'],
                'content': documents[doc_id]['content']
            }
            for doc_id in non_overlapping_docs
        ]

        return results

    @classmethod
    def proximal_node_search(cls, documents: List[dict], entities: List[str], window_size: int = 50):
        """
        Perform proximal node search with configurable window size.
        
        Args:
            documents (List[dict]): List of documents to search
            entities (List[str]): List of entities to find in proximity
            window_size (int): Maximum distance between entities
        
        Returns:
            Dict[str, List[dict]]: Dictionary of proximity search results
        """
        results = defaultdict(list)

        # Ensure we have at least two entities for proximity search
        if len(entities) < 2:
            return dict(results)

        for doc in documents:
            doc_lower = doc['content'].lower()
            doc_length = len(doc_lower)
            
            # Find all occurrences of each entity
            entity_positions = {}
            for entity in entities:
                entity_lower = entity.lower()
                positions = []
                start = 0
                while True:
                    pos = doc_lower.find(entity_lower, start)
                    if pos == -1:
                        break
                    positions.append(pos)
                    start = pos + 1
                if positions:
                    entity_positions[entity] = positions

            # Check for proximity between entities
            if len(entity_positions) >= 2:
                for i, (entity1, pos1_list) in enumerate(entity_positions.items()):
                    for entity2, pos2_list in list(entity_positions.items())[i+1:]:
                        for pos1 in pos1_list:
                            for pos2 in pos2_list:
                                if abs(pos1 - pos2) <= window_size:
                                    start_pos = max(0, min(pos1, pos2) - 20)
                                    end_pos = min(doc_length, max(pos1, pos2) + 20)
                                    context = doc['content'][start_pos:end_pos]
                                    
                                    result_entry = {
                                        'title': doc['filename'],
                                        'content': doc['content'],
                                        'context': context,
                                        'entities_found': [entity1, entity2],
                                        'distance': abs(pos1 - pos2)
                                    }
                                    
                                    key = f"{entity1}-{entity2}"
                                    results[key].append(result_entry)

        return dict(results)