# file: retriever.py

import pickle
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferWindowMemory
from langchain.chains import LLMChain


MODEL_NAME = "all-MiniLM-L6-v2"
OLLAMA_MODEL = "mistral"
TOP_K = 4


class ConversationalRAG:
    def __init__(self, index_folder="faiss_index"):
        print("Loading embedding model...")
        self.embed_model = SentenceTransformer(MODEL_NAME)

        print("Loading FAISS index...")
        self.index = faiss.read_index(f"{index_folder}/faiss.index")

        print("Loading metadata...")
        with open(f"{index_folder}/metadata.pkl", "rb") as f:
            self.metadata = pickle.load(f)

        print("Loading LLM...")
        self.llm = Ollama(model=OLLAMA_MODEL)

        # 🧠 Memory keeps last 5 interactions
        self.memory = ConversationBufferWindowMemory(
            k=5,
            memory_key="chat_history",
            return_messages=True
        )

        self.prompt_template = PromptTemplate(
            input_variables=["context", "question", "chat_history"],
            template="""
You are a helpful AI assistant.

Conversation so far:
{chat_history}

Use the context below to answer the question.
If the answer is not found, say "I don't know based on the documents."

Context:
{context}

Question:
{question}

Answer:
"""
        )

        self.chain = LLMChain(
            llm=self.llm,
            prompt=self.prompt_template,
            memory=self.memory
        )

    def embed_query(self, query: str):
        vector = self.embed_model.encode([query])
        return np.array(vector).astype("float32")

    def retrieve(self, query: str):
        query_vector = self.embed_query(query)
        distances, indices = self.index.search(query_vector, TOP_K)

        retrieved_chunks = []
        for idx in indices[0]:
            if idx < len(self.metadata):
                retrieved_chunks.append(self.metadata[idx]["text"])

        return retrieved_chunks

    def ask(self, query: str):
        context_chunks = self.retrieve(query)
        context = "\n\n".join(context_chunks)

        response = self.chain.invoke({
            "context": context,
            "question": query
        })

        return response["text"]


# ----------------------
# Test Chat Loop
# ----------------------
if __name__ == "__main__":
    rag = ConversationalRAG()

    print("\nConversational RAG ready. Type 'exit' to stop.\n")

    while True:
        query = input("You: ")
        if query.lower() == "exit":
            break

        answer = rag.ask(query)
        print("\nAssistant:", answer, "\n")
