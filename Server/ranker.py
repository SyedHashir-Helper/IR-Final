import os
import math
import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords

nltk.download('punkt')
nltk.download('stopwords')

class DocumentRanker:
    def __init__(self, documents):
        """
        Initialize DocumentRanker with a list of documents
        
        :param documents: List of dictionaries with 'title' and 'content' keys
        """
        self.documents = documents
    
    def preprocess_text(self, text):
        """
        Preprocess text by tokenizing, converting to lowercase, 
        removing punctuation and stopwords
        
        :param text: Input text string
        :return: List of preprocessed tokens
        """
        tokens = word_tokenize(text)
        
        # Convert to lowercase and remove punctuation
        tokens = [word.lower() for word in tokens if word.isalnum()]
        
        # Remove stopwords
        stop_words = set(stopwords.words('english'))
        filtered_tokens = [word for word in tokens if word not in stop_words]
        
        return filtered_tokens
    
    def calculate_tf(self, word, document):
        """
        Calculate Term Frequency (TF)
        
        :param word: Word to calculate TF for
        :param document: Preprocessed document (as a string)
        :return: Term Frequency
        """
        return document.split().count(word) / len(document.split())
    
    def calculate_idf(self, word):
        """
        Calculate Inverse Document Frequency (IDF)
        
        :param word: Word to calculate IDF for
        :return: Inverse Document Frequency
        """
        # Count documents containing the word
        doc_count = sum(1 for doc in self.documents if word in doc['preprocessed_content'].split())
        total_docs = len(self.documents)
        
        if doc_count == 0:
            return 0
        return math.log(total_docs / doc_count)
    
    def preprocess_documents(self):
        """
        Preprocess all documents by adding preprocessed_content
        """
        for doc in self.documents:
            doc['preprocessed_content'] = ' '.join(self.preprocess_text(doc['content']))
    
    def keyword_matching(self, query):
        """
        Perform keyword matching search
        
        :param query: Search query string
        :return: Ranked list of documents
        """
        query_keywords = self.preprocess_text(query)
        if 'preprocessed_content' not in self.documents[0]:
            self.preprocess_documents()
        # Rank documents based on keyword matches
        rankings = []
        for doc in self.documents:
            doc_words = doc['preprocessed_content'].split()
            match_count = sum(doc_words.count(keyword) for keyword in query_keywords if keyword in doc_words)
            rankings.append((doc, match_count))
        
        # Sort by match count in descending order
        rankings.sort(key=lambda x: x[1], reverse=True)
        print("Ranking") 
        return rankings
    
    def calculate_tf_idf(self, query):
        """
        Perform TF-IDF ranking search
        
        :param query: Search query string
        :return: Ranked list of documents with TF-IDF scores
        """
        # Preprocess documents if not already done
        if 'preprocessed_content' not in self.documents[0]:
            self.preprocess_documents()
        
        query_keywords = self.preprocess_text(query)
        
        # Calculate TF-IDF scores
        scores = {}
        for doc in self.documents:
            doc_words = doc['preprocessed_content'].split()
            tf_idf_score = 0
            for keyword in query_keywords:
                # Only calculate for keywords present in document
                if keyword in doc_words:
                    tf = self.calculate_tf(keyword, doc['preprocessed_content'])
                    idf = self.calculate_idf(keyword)
                    tf_idf_score += tf * idf
            
            # Only add if score is non-zero
            if tf_idf_score > 0:
                scores[doc['title']] = tf_idf_score
        
        # Sort scores in descending order
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        
        # Return documents in sorted order
        return [doc for doc, _ in sorted_scores]