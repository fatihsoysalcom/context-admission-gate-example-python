import re

def tokenize(text: str) -> set[str]:
    """Simple tokenizer: lowercase and split by non-alphanumeric characters."""
    return set(re.findall(r'\b\w+\b', text.lower()))

def context_admission_gate(query: str, documents: list[str], min_shared_keywords: int = 1) -> list[str]:
    """
    Simulates a 'Context Admission Gate' by filtering documents based on relevance to a query.
    Documents are admitted if they share at least `min_shared_keywords` with the query.
    This prevents irrelevant information from entering an AI model's context window.
    """
    query_keywords = tokenize(query)
    admitted_documents = []
    print(f"--- Context Admission Gate Processing ---")
    print(f"Query: '{query}'")
    print(f"Query Keywords for filtering: {query_keywords}")

    for i, doc in enumerate(documents):
        doc_keywords = tokenize(doc)
        # Calculate intersection of keywords to determine relevance
        shared_keywords = query_keywords.intersection(doc_keywords)
        relevance_score = len(shared_keywords)

        print(f"\nDocument {i+1} (first 70 chars): '{doc[:70]}...' ")
        print(f"Document Keywords: {doc_keywords}")
        print(f"Shared Keywords with query: {shared_keywords} (Relevance Score: {relevance_score})")

        # This is the core 'admission gate' logic:
        # Only documents meeting the relevance threshold are passed through.
        if relevance_score >= min_shared_keywords:
            admitted_documents.append(doc)
            print(f"-> ADMITTED (Score {relevance_score} >= Threshold {min_shared_keywords}) - Will enter AI model's context")
        else:
            print(f"-> REJECTED (Score {relevance_score} < Threshold {min_shared_keywords}) - Will NOT enter AI model's context")

    return admitted_documents

# --- Example Usage ---
if __name__ == "__main__":
    # Simulate a collection of potential documents/files for an AI model
    all_documents = [
        "Python is a high-level, interpreted programming language. It's great for web development and data science.",
        "JavaScript is a programming language that is one of the core technologies of the World Wide Web, alongside HTML and CSS.",
        "The recipe for a perfect chocolate cake involves flour, sugar, eggs, and cocoa powder. Bake at 180C for 30 minutes.",
        "Understanding data structures like lists, dictionaries, and sets is crucial for efficient Python programming.",
        "Rust is a multi-paradigm, general-purpose programming language designed for performance and safety, especially safe concurrency.",
        "Learn about Python's powerful libraries like NumPy and Pandas for numerical computing and data analysis.",
        "How to make a delicious pasta carbonara: eggs, cheese, pancetta, and black pepper. No cream!",
        "Python's simplicity and readability make it an excellent choice for beginners and experienced developers alike."
    ]

    # The query or task for which the AI model needs relevant context
    user_query = "Tell me about Python programming and its applications in data science."

    print("--- All Available Documents (Potential Context) ---")
    for i, doc in enumerate(all_documents):
        print(f"Document {i+1}: {doc[:80]}...")
    print("\n" + "="*80 + "\n")

    # Apply the Context Admission Gate to filter documents
    # We set a threshold of 2 shared keywords for a document to be considered relevant,
    # simulating a stricter filter for the AI model's context window.
    admitted_docs = context_admission_gate(user_query, all_documents, min_shared_keywords=2)

    print("\n" + "="*80 + "\n")
    print("--- Admitted Documents for AI Model's Context Window ---")
    if admitted_docs:
        for i, doc in enumerate(admitted_docs):
            print(f"Admitted Document {i+1}: {doc[:80]}...")
    else:
        print("No documents were admitted based on the current criteria.")

    print("\n" + "="*80 + "\n")
    print(f"Total original documents considered: {len(all_documents)}")
    print(f"Total documents admitted to context: {len(admitted_docs)}")
