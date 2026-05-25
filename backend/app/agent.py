from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
import operator
import os
from dotenv import load_dotenv
from app.knowledge_base import retrieve_relevant_docs

load_dotenv()

# Define the state that flows through the agent graph
class AgentState(TypedDict):
    messages: Annotated[list, operator.add]
    user_query: str
    retrieved_docs: list[str]
    final_response: str

# Initialize the LLM
llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.1-8b-instant"
)

# --- Node 1: Retrieve relevant docs from ChromaDB ---
def retrieve_node(state: AgentState) -> AgentState:
    query = state["user_query"]
    docs = retrieve_relevant_docs(query)
    return {"retrieved_docs": docs}

# --- Node 2: Generate a response using the LLM ---
def generate_node(state: AgentState) -> AgentState:
    query = state["user_query"]
    docs = state["retrieved_docs"]

    # Build context from retrieved docs
    context = "\n\n".join(docs) if docs else "No relevant documents found."

    system_prompt = """You are a helpful customer support agent. 
Use the provided context from the knowledge base to answer the user's question accurately.
If the context does not contain enough information, say so honestly and suggest contacting support.
Keep your responses clear, concise, and friendly."""

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"Context from knowledge base:\n{context}\n\nUser question: {query}")
    ]

    response = llm.invoke(messages)
    return {"final_response": response.content}

# --- Build the LangGraph graph ---
def build_agent():
    graph = StateGraph(AgentState)

    graph.add_node("retrieve", retrieve_node)
    graph.add_node("generate", generate_node)

    graph.set_entry_point("retrieve")
    graph.add_edge("retrieve", "generate")
    graph.add_edge("generate", END)

    return graph.compile()

# Compile the agent once at startup
agent = build_agent()

def run_agent(user_query: str) -> dict:
    """Run the agent and return the response and sources."""
    result = agent.invoke({
        "messages": [],
        "user_query": user_query,
        "retrieved_docs": [],
        "final_response": ""
    })
    return {
        "response": result["final_response"],
        "sources": result["retrieved_docs"]
    }