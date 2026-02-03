from typing import TypedDict
from langgraph.graph import StateGraph, END

from langchain_community.llms import Ollama

from rag_agent.retriever import ConversationalRAG
from sql_agent.query_agent import SQLQueryAgent


# ---------------- STATE ----------------
class AgentState(TypedDict):
    question: str
    route: str
    answer: str


# ---------------- LOAD AGENTS ----------------
rag_agent = ConversationalRAG()
sql_agent = SQLQueryAgent()
llm_router = Ollama(model="mistral")


# ---------------- ROUTER NODE ----------------
def router_node(state: AgentState):
    question = state["question"]

    routing_prompt = f"""
Decide the question type.

If question involves:
- numbers
- calculations
- totals, averages, sums
- tables, rows, columns
→ respond with SQL

If question is about documents, text, explanation
→ respond with RAG

Question: {question}
Answer only: SQL or RAG
"""

    decision = llm_router.invoke(routing_prompt).strip().upper()

    if "SQL" in decision:
        route = "sql"
    else:
        route = "rag"

    return {"route": route}


# ---------------- RAG NODE ----------------
def rag_node(state: AgentState):
    answer = rag_agent.ask(state["question"])
    return {"answer": answer}


# ---------------- SQL NODE ----------------
def sql_node(state: AgentState):
    result = sql_agent.ask(state["question"])
    return {"answer": str(result)}


# ---------------- GRAPH BUILD ----------------
builder = StateGraph(AgentState)

builder.add_node("router", router_node)
builder.add_node("rag", rag_node)
builder.add_node("sql", sql_node)

builder.set_entry_point("router")

builder.add_conditional_edges(
    "router",
    lambda state: state["route"],
    {
        "rag": "rag",
        "sql": "sql"
    }
)

builder.add_edge("rag", END)
builder.add_edge("sql", END)

graph = builder.compile()


# ---------------- TEST LOOP ----------------
if __name__ == "__main__":
    print("\nAgentic AI System Ready. Type 'exit' to stop.\n")

    while True:
        q = input("You: ")
        if q.lower() == "exit":
            break

        result = graph.invoke({"question": q})
        print("\nAssistant:", result["answer"], "\n")
