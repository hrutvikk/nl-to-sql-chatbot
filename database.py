#This file has one job i.e to load our .csv file to SQLite database.

import pandas as pd
from sqlalchemy import create_engine, text

#This function is use to load the data from CSV to the db
def load_data_to_db(csv_path="data/superstore.csv",db_path="data/superstore.db"):
    print("Reading CSV file...") 
    df = pd.read_csv(csv_path,encoding="latin-1")
    df.columns = df.columns.str.strip().str.replace(" ","_").str.replace("-","_") #Standardizing the columns
    # Lets check what we have loaded so  far
    print(f"Loaded {len(df)} rows and {len(df.columns)} columns.")
    print("Columns:", list(df.columns))
    #Lets create a connection to the database
    engine = create_engine(f"sqlite:///{db_path}")
    #Lets write the data into dataset and call it sales
    df.to_sql("sales",engine, if_exists="replace",index=False)
    print(f"Data is written to {db_path} and the table name is 'sales'")
    print("\nRunning test query...")
    with engine.connect() as conn:
        result = conn.execute(text("SELECT Region, COUNT(*) as order_count FROM sales GROUP BY Region"))
        rows = result.fetchall()
        print("\nOrders per region:")
        for row in rows:
            print(f"  {row[0]}: {row[1]} orders")

    print("\nDatabase setup complete!")

# This means: only run the function if we run THIS file directly
# (not when another file imports it)
if __name__ == "__main__":
    load_data_to_db()


    