from typing import List, Set, Dict, Any


def preprocess_document(doc: str) -> Set[str]:
    """
    Convert document to lowercase and tokenize it into a set of words.
    """
    return set(doc.lower().split())


def boolean_and(set1: Set[int], set2: Set[int]) -> Set[int]:
    """
    Perform AND operation on two sets.
    """
    return set1.intersection(set2)


def boolean_or(set1: Set[int], set2: Set[int]) -> Set[int]:
    """
    Perform OR operation on two sets.
    """
    return set1.union(set2)


def boolean_not(set1: Set[int], universe: Set[int]) -> Set[int]:
    """
    Perform NOT operation relative to the universe of document indices.
    """
    return universe.difference(set1)


def infix_to_postfix(query_tokens: List[str]) -> List[str]:
    """
    Convert an infix Boolean query to postfix notation for evaluation.
    """
    precedence = {'not': 3, 'and': 2, 'or': 1}
    output = []
    operators = []
    
    for token in query_tokens:
        if token in ['and', 'or', 'not']:
            while (operators and operators[-1] != '(' and
                   precedence[token] <= precedence[operators[-1]]):
                output.append(operators.pop())
            operators.append(token)
        elif token == '(':
            operators.append(token)
        elif token == ')':
            while operators and operators[-1] != '(':
                output.append(operators.pop())
            operators.pop()  # Pop '('
        else:
            output.append(token)
    
    while operators:
        output.append(operators.pop())
    
    return output


def evaluate_postfix(postfix_tokens: List[str], processed_docs: List[Set[str]], universe: Set[int]) -> Set[int]:
    """
    Evaluate a Boolean query in postfix notation against processed documents.
    """
    stack = []
    
    for token in postfix_tokens:
        if token in ['and', 'or', 'not']:
            if token == 'not':
                set1 = stack.pop()
                stack.append(boolean_not(set1, universe))
            else:
                set2 = stack.pop()
                set1 = stack.pop()
                if token == 'and':
                    stack.append(boolean_and(set1, set2))
                elif token == 'or':
                    stack.append(boolean_or(set1, set2))
        else:  # Token is a term
            term_set = set(idx for idx, doc in enumerate(processed_docs) if token in doc)
            stack.append(term_set)
    
    return stack[0]


def process_query(query: str, processed_docs: List[Set[str]]) -> Set[int]:
    """
    Parse and process a Boolean query, returning matching document indices.
    """
    query_tokens = query.lower().split()
    universe = set(range(len(processed_docs)))
    postfix_tokens = infix_to_postfix(query_tokens)
    return evaluate_postfix(postfix_tokens, processed_docs, universe)
