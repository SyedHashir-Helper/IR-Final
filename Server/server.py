from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
from collections import defaultdict, Counter
from nltk import word_tokenize, pos_tag
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer
import math
from bim import DocumentSearcher
from ranker import DocumentRanker
from ir_helper import InformationRetrievalModels
from boolean import preprocess_document, process_query

app = Flask(__name__)
cors = CORS(app)  # Enable CORS for all routes

documents = []  # In-memory storage for documents

@app.route('/api/documents/upload', methods=['POST'])
def upload_documents():
    data = request.get_json()  # Get the JSON data from the request
    uploaded_docs = []
    # Check if data was received
    if not data:
        return jsonify({"error": "No data received"}), 400

    for item in data['files']:  # Adjust to access 'files' from the received payload
        try:
            filename = item.get('filename')
            content = item.get('content')
            if not filename or not content:
                return jsonify({"error": "Missing filename or content in the uploaded data"}), 400

            doc = {
                "title": filename,
                "content": content
            }
            documents.append(doc)
            uploaded_docs.append(doc['title'])
        except Exception as e:
            return jsonify({"error": f"Error processing file {filename}: {str(e)}"}), 500

    return jsonify({
        "message": f"Successfully uploaded {len(uploaded_docs)} documents",
        "uploaded_documents": uploaded_docs
    }), 201


@app.route('/documents/list', methods=['GET'])
def list_documents():
    return jsonify(documents), 200

@app.route('/api/documents/search/title', methods=['POST'])
def search_by_title():
    query = request.args.get('query', '').lower()
    results = [doc for doc in documents if query in doc['title'].lower()]
    return jsonify(results), 200

@app.route('/api/documents/search/content', methods=['POST'])
def search_by_content():
    query = request.json.get('query', '').lower()

    def get_synonyms(word):
        synonyms = set()
        for syn in wordnet.synsets(word):
            for lemma in syn.lemmas():
                synonyms.add(lemma.name().lower())
        return list(synonyms)

    def expand_query_with_synonyms(query_tokens):
        expanded_query = set(query_tokens)
        for word in query_tokens:
            expanded_query.update(get_synonyms(word))
        return list(expanded_query)

    def extract_nouns_and_entities(content):
        words = word_tokenize(content.lower())
        pos_tags = pos_tag(words)
        nouns = [word for word, pos in pos_tags if pos in ('NN', 'NNS', 'NNP', 'NNPS')]
        lemmatizer = WordNetLemmatizer()
        lemmatized_nouns = [lemmatizer.lemmatize(noun) for noun in nouns]
        return lemmatized_nouns

    def calculate_tf(doc_words):
        tf = {}
        total_words = len(doc_words)
        word_counts = Counter(doc_words)
        for word, count in word_counts.items():
            tf[word] = count / total_words
        return tf

    def calculate_idf(documents):
        idf = {}
        total_docs = len(documents)
        word_doc_counts = defaultdict(int)
        for doc_words in documents:
            unique_words = set(doc_words)
            for word in unique_words:
                word_doc_counts[word] += 1
        for word, doc_count in word_doc_counts.items():
            idf[word] = math.log(total_docs / (1 + doc_count))
        return idf

    def calculate_tfidf(doc_words, tf, idf):
        tfidf = {}
        for word in doc_words:
            if word in idf:
                tfidf[word] = tf[word] * idf[word]
        return tfidf

    query_tokens = word_tokenize(query)
    expanded_query = expand_query_with_synonyms(query_tokens)

    matching_docs = []
    for doc in documents:
        doc_words = extract_nouns_and_entities(doc['content'])
        tf = calculate_tf(doc_words)
        idf = calculate_idf([doc_words])
        tfidf = calculate_tfidf(doc_words, tf, idf)

        if any(word in tfidf for word in expanded_query):
            matching_docs.append(doc)

    return jsonify(matching_docs), 200


@app.route('/api/bim', methods=['POST'])
def search_documents():
    """
    Handle document search
    """
    
    try:
        # Get request data
        data = request.get_json()
        query = data.get('query', '')
        
        if not query:
            return jsonify({"error": "No query provided"}), 400
        
        if not documents:
            return jsonify({"error": "No documents uploaded"}), 400
        print(documents)
        # Perform binary term matching search
        results = DocumentSearcher.binary_term_matching(documents=documents, query=query)
        
        return jsonify(results), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/non-overlapping-search', methods=['POST'])
def non_overlapping_search():
    """
    Handle non-overlapping lists search
    """
    global documents
    
    try:
        # Get request data
        data = request.get_json()
        terms = data.get('query', '')
        
        if not terms:
            return jsonify({"error": "No search terms provided"}), 400
        
        if not documents:
            return jsonify({"error": "No documents uploaded"}), 400
        
        # Perform non-overlapping lists search
        results = DocumentSearcher.non_overlapping_lists_search(documents=documents, terms=terms.split(' '))
        
        return jsonify(results), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/proximal-node-search', methods=['POST'])
def proximal_node_search():
    """
    Handle proximal node search
    """
    global uploaded_files
    
    try:
        # Get request data
        data = request.get_json()
        entities = data.get('entities', [])
        window_size = data.get('window_size', 50)
        
        if not entities:
            return jsonify({"error": "No entities provided"}), 400
        
        if not uploaded_files:
            return jsonify({"error": "No documents uploaded"}), 400
        
        # Perform proximal node search
        results = DocumentSearcher.proximal_node_search(uploaded_files, entities, window_size)
        
        return jsonify(results), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/search/keyword', methods=['POST'])
def keyword_matching():
    """
    Endpoint for keyword matching search
    """
    data = request.get_json()
    query = data.get('query')
    print(query)
    
    if not query:
        return jsonify({"error": "No search query provided"}), 400
    
    try:
        print("Document Ranker Enter")
        # Initialize DocumentRanker
        ranker = DocumentRanker(documents=documents)
        print("Keyword Matching Start")
        # Perform keyword matching
        rankings = ranker.keyword_matching(query)
        print()
        # Prepare response
        results = [
            {
                'title': doc['title'], 
                'content': doc['content']
            } for doc, _ in rankings
        ]
        print("Result")
        return jsonify(results)
    
    except Exception as e:
        return jsonify({"error": f"Search failed: {str(e)}"}), 500

@app.route('/api/search/tfidf', methods=['POST'])
def tf_idf_ranking():
    """
    Endpoint for TF-IDF ranking search
    """
    data = request.get_json()
    query = data.get('query')
    
    if not query:
        return jsonify({"error": "No search query provided"}), 400
    
    try:
        # Initialize DocumentRanker
        ranker = DocumentRanker(documents=documents)
        
        # Perform TF-IDF ranking
        rankings = ranker.calculate_tf_idf(query)
        
        # Prepare response
        results = [
            {
                'title': doc['title'], 
                'content': doc['content']
            } for doc in documents if doc['title'] in rankings
        ]
        
        return jsonify(results)
    
    except Exception as e:
        return jsonify({"error": f"Search failed: {str(e)}"}), 500

@app.route('/api/search/interference', methods=['POST'])
def search_interference():
    """
    Endpoint to perform interference model search.
    """
    if not documents:
        return jsonify({"error": "No documents available"}), 400

    query = request.json.get('query')
    if not query:
        return jsonify({"error": "No query provided"}), 400

    # Initialize IR model
    ir_model = InformationRetrievalModels([(doc['title'], doc['content']) for doc in documents])
    ir_model.create_relevance_judgments([query])

    results = ir_model.interference_model(query)
    response = [{"title": documents[idx]['title'], "content": documents[idx]['content'], "score": score} for idx, score in results if score > 0]

    return jsonify(response), 200

@app.route('/api/search/belief', methods=['POST'])
def search_belief():
    """
    Endpoint to perform belief network search.
    """
    if not documents:
        return jsonify({"error": "No documents available"}), 400
    
    query = request.json.get('query')
    if not query:
        return jsonify({"error": "No query provided"}), 400
    
    # Initialize IR model
    ir_model = InformationRetrievalModels([(doc['title'], doc['content']) for doc in documents])
    ir_model.create_relevance_judgments([query])
    
    results = ir_model.belief_network(query)
    response = [{"title": documents[idx]['title'], "content": documents[idx]['content'], "score": score} for idx, score in results if score > 0]
    
    return jsonify(response), 200

@app.route('/api/search/boolean', methods=['POST'])
def process_query_endpoint():
    try:
        data = request.get_json()
        query = data.get('query', '')
        
        if not query:
            return jsonify({"error": "Query is required"}), 400
        
        processed_docs = [preprocess_document(doc['content']) for doc in documents]
        # Process the query and retrieve matching document indices
        result_set = process_query(query, processed_docs)
        matching_docs = [{'title': documents[idx]['title'], 'content': documents[idx]['content']} for idx in result_set]
        
        return jsonify(matching_docs), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
