
import pandas as pd
from sqlalchemy import create_engine, text


class DatabaseManager:
    def __init__(self,
                 user="postgres",
                 password="postgres",
                 host="localhost",
                 port="5432",
                 database="rag_sql_db"):
        
        self.engine = create_engine(
            f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"
        )

    def upload_csv_to_db(self, csv_path: str, table_name: str):
        """
        Reads CSV and creates table in PostgreSQL
        """
        df = pd.read_csv(csv_path)

        df.to_sql(
            table_name,
            self.engine,
            if_exists="replace",
            index=False
        )

        print(f"Uploaded {csv_path} to table '{table_name}'")

    def execute_query(self, sql_query: str):
        """
        Runs SQL query and returns result
        """
        with self.engine.connect() as conn:
            result = conn.execute(text(sql_query))
            rows = result.fetchall()
            columns = result.keys()

        return [dict(zip(columns, row)) for row in rows]
