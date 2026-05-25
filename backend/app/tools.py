from langchain_core.tools import tool
from app.knowledge_base import retrieve_relevant_docs
from datetime import datetime

@tool
def search_knowledge_base(query: str) -> str:
    """Search the customer support knowledge base for information relevant to the user's question.
    Use this for questions about passwords, billing, accounts, technical issues, or any product-related queries."""
    docs = retrieve_relevant_docs(query)
    if not docs:
        return "No relevant information found in the knowledge base."
    return "\n\n".join(docs)

@tool
def get_current_datetime() -> str:
    """Get the current date and time. Use this when the user asks about the current time or date."""
    now = datetime.now()
    return f"Current date and time: {now.strftime('%A, %B %d, %Y at %I:%M %p')}"

@tool
def escalate_to_human(reason: str) -> str:
    """Escalate the conversation to a human support agent when you cannot resolve the issue.
    Use this when the user is frustrated, the issue is complex, or you don't have enough information to help."""
    return f"I've flagged this conversation for human review. Reason: {reason}. A human support agent will follow up with you shortly via email."

@tool
def lookup_faq(topic: str) -> str:
    """Look up frequently asked questions for common topics like refunds, shipping, pricing, or account issues."""
    faqs = {
        "refund": "Our refund policy allows returns within 30 days of purchase. Contact support@example.com with your order number to initiate a refund.",
        "pricing": "We offer three plans: Basic ($9/month), Pro ($29/month), and Enterprise (custom pricing). All plans include a 14-day free trial.",
        "shipping": "Standard shipping takes 5-7 business days. Express shipping (2-3 days) is available for an additional $10.",
        "account deletion": "To delete your account, go to Settings > Account > Delete Account. Note that this action is irreversible and all data will be permanently removed.",
        "payment methods": "We accept all major credit cards (Visa, Mastercard, Amex), PayPal, and bank transfers for Enterprise plans.",
    }
    topic_lower = topic.lower()
    for key, value in faqs.items():
        if key in topic_lower or topic_lower in key:
            return value
    return f"No FAQ found for '{topic}'. Try searching the knowledge base instead."

# List of all tools for the agent
tools = [search_knowledge_base, get_current_datetime, escalate_to_human, lookup_faq]