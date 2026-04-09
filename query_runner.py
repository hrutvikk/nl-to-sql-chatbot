#This file the SQL Query as a String and Return the Results

import pandas as pd
from sqlalchemy import create_engine, text

db_path = "data/superstore.db"

def run_query(sql: str) -> pd.DataFrame:
    """
    This takes query from the user run it on our superstore.db and will return a
    #a pandas dataframe
    """
    #Connecting to database
    engine = create_engine(f"sqlite:///{db_path}")

    try:
        with engine.connect() as conn:
            df = pd.read_sql(text(sql),conn)
            return df
    except Exception as e:
        print(f"Query Failed {e}")
        return pd.DataFrame #Returns Empty dataframe so the app dosnt crash

def preview_table(rows: int = 5) -> pd.DataFrame:

    return run_query(f"Select * From sales LIMIT {rows}")

def get_schema() -> str:
    engine = create_engine(f'sqlite:///{db_path}')
    with engine.connect() as conn:
        result = conn.execute(text("PRAGMA table_info(sales)"))
        rows = result.fetchall()
        #Format as readable String
    schema_lines = [f"{row[1]} ({row[2]})" for row in rows]
    schema_str = "Table: sales\nColumns:\n" + "\n".join(f"  - {line}" for line in schema_lines)
    return schema_str

#Testing all 3 Functions
if __name__ == "__main__":

    print("=" * 50)
    print("TABLE SCHEMA")
    print("=" * 50)
    print(get_schema())

    print("\n" + "=" * 50)
    print("FIRST 5 ROWS")
    print("=" * 50)
    df_preview = preview_table(5)
    print(df_preview.to_string())

    print("\n" + "=" * 50)
    print("TEST QUERY: Top 5 regions by total sales")
    print("=" * 50)
    df_result = run_query("""
        SELECT Region, ROUND(SUM(Sales), 2) as Total_Sales
        FROM sales
        GROUP BY Region
        ORDER BY Total_Sales DESC
        LIMIT 5
    """)
    print(df_result.to_string())