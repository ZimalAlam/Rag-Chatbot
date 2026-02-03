from fastapi import APIRouter
from app.agents.agent_graph import graph

router = APIRouter()

@router.post("/chat/")
async def chat(query: str):
    result = graph.invoke({"question": query})
    return {"answer": result["answer"]}
