
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

from .db import DatabaseManager


OLLAMA_MODEL = "mistral"


class SQLQueryAgent:
    def __init__(self):
        self.db = DatabaseManager()
        self.llm = Ollama(model=OLLAMA_MODEL)

        self.prompt = PromptTemplate(
            input_variables=["schema", "question"],
            template="""
You are a SQL expert.

Given the database schema below, write a correct PostgreSQL query.

Schema:
{schema}

Question:
{question}

SQL Query:
"""
        )

        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)

    def get_schema_description(self):
        """
        Get tables + columns from database
        """
        query = """
        SELECT table_name, column_name, data_type
        FROM information_schema.columns
        WHERE table_schema = 'public';
        """
        result = self.db.execute_query(query)

        schema = ""
        for row in result:
            schema += f"Table {row['table_name']} - Column {row['column_name']} ({row['data_type']})\n"

        return schema

    def ask(self, question: str):
        schema = self.get_schema_description()

        sql_query = self.chain.invoke({
            "schema": schema,
            "question": question
        })["text"]

        print("Generated SQL:", sql_query)

        result = self.db.execute_query(sql_query)
        return result
