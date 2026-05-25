# from langchain_groq import ChatGroq
# from langchain_core.messages import HumanMessage, SystemMessage
# from langgraph.graph import StateGraph, END
# from typing import TypedDict, Annotated
# import operator
# import os
# from dotenv import load_dotenv
# from app.knowledge_base import retrieve_relevant_docs

# load_dotenv()

# # Define the state that flows through the agent graph
# class AgentState(TypedDict):
#     messages: Annotated[list, operator.add]
#     user_query: str
#     retrieved_docs: list[str]
#     final_response: str

# # Initialize the LLM
# llm = ChatGroq(
#     api_key=os.getenv("GROQ_API_KEY"),
#     model_name="llama-3.1-8b-instant"
# )

# # --- Node 1: Retrieve relevant docs from ChromaDB ---
# def retrieve_node(state: AgentState) -> AgentState:
#     query = state["user_query"]
#     docs = retrieve_relevant_docs(query)
#     return {"retrieved_docs": docs}

# # --- Node 2: Generate a response using the LLM ---
# def generate_node(state: AgentState) -> AgentState:
#     query = state["user_query"]
#     docs = state["retrieved_docs"]

#     # Build context from retrieved docs
#     context = "\n\n".join(docs) if docs else "No relevant documents found."

#     system_prompt = """You are a helpful customer support agent. 
# Use the provided context from the knowledge base to answer the user's question accurately.
# If the context does not contain enough information, say so honestly and suggest contacting support.
# Keep your responses clear, concise, and friendly."""

#     messages = [
#         SystemMessage(content=system_prompt),
#         HumanMessage(content=f"Context from knowledge base:\n{context}\n\nUser question: {query}")
#     ]

#     response = llm.invoke(messages)
#     return {"final_response": response.content}

# # --- Build the LangGraph graph ---
# def build_agent():
#     graph = StateGraph(AgentState)

#     graph.add_node("retrieve", retrieve_node)
#     graph.add_node("generate", generate_node)

#     graph.set_entry_point("retrieve")
#     graph.add_edge("retrieve", "generate")
#     graph.add_edge("generate", END)

#     return graph.compile()

# # Compile the agent once at startup
# agent = build_agent()

# def run_agent(user_query: str) -> dict:
#     """Run the agent and return the response and sources."""
#     result = agent.invoke({
#         "messages": [],
#         "user_query": user_query,
#         "retrieved_docs": [],
#         "final_response": ""
#     })
#     return {
#         "response": result["final_response"],
#         "sources": result["retrieved_docs"]
#     }




from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage, ToolMessage
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from typing import TypedDict, Annotated
import operator
import os
from dotenv import load_dotenv
from app.tools import tools

load_dotenv()

# Define the state that flows through the agent graph
class AgentState(TypedDict):
    messages: Annotated[list, operator.add]

# Initialize the LLM with tools bound to it
llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.3-70b-versatile"
)

llm_with_tools = llm.bind_tools(tools)

SYSTEM_PROMPT = """You are a helpful customer support agent with access to the following tools:

1. search_knowledge_base - Search for product/service support information
2. get_current_datetime - Get the current date and time
3. escalate_to_human - Escalate complex issues to a human agent
4. lookup_faq - Look up frequently asked questions

Always try to use the most appropriate tool to answer the user's question accurately.
If you cannot find relevant information, use escalate_to_human.
Be friendly, concise, and professional."""

# --- Node 1: Call the LLM ---
def call_llm(state: AgentState) -> AgentState:
    messages = [SystemMessage(content=SYSTEM_PROMPT)] + state["messages"]
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

# --- Node 2: Tool execution node ---
tool_node = ToolNode(tools)

# --- Routing: decide whether to call tools or end ---
def should_continue(state: AgentState) -> str:
    last_message = state["messages"][-1]
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"
    return "end"

# --- Build the LangGraph graph ---
def build_agent():
    graph = StateGraph(AgentState)

    graph.add_node("llm", call_llm)
    graph.add_node("tools", tool_node)

    graph.set_entry_point("llm")

    graph.add_conditional_edges(
        "llm",
        should_continue,
        {
            "tools": "tools",
            "end": END
        }
    )

    graph.add_edge("tools", "llm")

    return graph.compile()

# Compile the agent once at startup
agent = build_agent()

def run_agent(user_query: str) -> dict:
    """Run the agent and return the response and sources."""
    result = agent.invoke({
        "messages": [HumanMessage(content=user_query)]
    })

    # Extract the final text response
    final_message = result["messages"][-1]
    response_text = final_message.content

    # Extract any tool results as sources
    sources = []
    for msg in result["messages"]:
        if isinstance(msg, ToolMessage):
            if msg.name == "search_knowledge_base":
                sources.append(msg.content)

    return {
        "response": response_text,
        "sources": sources
    }