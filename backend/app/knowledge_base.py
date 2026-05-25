import chromadb
from chromadb.utils import embedding_functions
import os

# Initialize ChromaDB client (stores data locally in a folder called chroma_db)
client = chromadb.PersistentClient(path="./chroma_db")

# Use sentence-transformers to convert text into vectors
embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

# Create or load the collection (like a table in a regular database)
collection = client.get_or_create_collection(
    name="support_docs",
    embedding_function=embedding_fn
)

# Sample support documents — these simulate a real knowledge base
SAMPLE_DOCS = [
    {
        "id": "1",
        "text": "To reset your password, go to the login page and click 'Forgot Password'. Enter your email address and you will receive a reset link within 5 minutes.",
        "metadata": {"category": "account"}
    },
    {
        "id": "2",
        "text": "To cancel your subscription, go to Settings > Billing > Cancel Subscription. Your access will continue until the end of the current billing period.",
        "metadata": {"category": "billing"}
    },
    {
        "id": "3",
        "text": "If you are experiencing slow performance, try clearing your browser cache, disabling browser extensions, or switching to a different browser.",
        "metadata": {"category": "technical"}
    },
    {
        "id": "4",
        "text": "To upgrade your plan, go to Settings > Billing > Upgrade Plan. You can choose from Basic, Pro, or Enterprise plans.",
        "metadata": {"category": "billing"}
    },
    {
        "id": "5",
        "text": "Our support team is available Monday to Friday, 9am to 6pm EST. You can reach us via email at support@example.com or through this chat.",
        "metadata": {"category": "general"}
    },
    {
        "id": "6",
        "text": "To export your data, go to Settings > Data > Export. You can export in CSV or JSON format. Large exports may take up to 10 minutes.",
        "metadata": {"category": "data"}
    },
    {
        "id": "7",
        "text": "Two-factor authentication can be enabled in Settings > Security > Enable 2FA. We support authenticator apps like Google Authenticator and Authy.",
        "metadata": {"category": "security"}
    },
    {
        "id": "8",
        "text": "If you cannot log in, make sure your caps lock is off, clear your browser cookies, and try again. If the issue persists, reset your password.",
        "metadata": {"category": "account"}
    }
]

def populate_knowledge_base():
    """Add sample docs to ChromaDB if not already added."""
    existing = collection.count()
    if existing == 0:
        collection.add(
            ids=[doc["id"] for doc in SAMPLE_DOCS],
            documents=[doc["text"] for doc in SAMPLE_DOCS],
            metadatas=[doc["metadata"] for doc in SAMPLE_DOCS]
        )
        print(f"Added {len(SAMPLE_DOCS)} documents to knowledge base.")
    else:
        print(f"Knowledge base already has {existing} documents.")

def retrieve_relevant_docs(query: str, n_results: int = 3) -> list[str]:
    """Retrieve the most relevant documents for a given query."""
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )
    return results["documents"][0] if results["documents"] else []