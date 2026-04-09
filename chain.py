"""This file take plain english question ask GPT-4o to write SQL for it
   Run that SQL and return the result
"""

import os
from openai import OpenAI
from dotenv import load_dotenv
from query_runner import run_query, get_schema

load_dotenv() #Loading API KEY
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def ask(question: str) -> dict:
    """
    Takes a plain English question.
    Returns a dict with:
      - 'sql'     : the SQL query GPT-4o wrote
      - 'result'  : a pandas DataFrame with the query results
      - 'answer'  : a plain English answer GPT-4o wrote from the results
      - 'error'   : any error message (empty string if no error)
    """
    schema = get_schema()
    """
    The Most Important part that is the prompting the entire result of our project depends upon 
    how good the pormpt is:
    """
    prompt = f"""You are a SQL expert. A user will ask a question about a sales dataset.
Your job is to write a single SQLite SQL query that answers their question.

Here is the database schema:
{schema}

Rules you must follow:
1. Return ONLY the raw SQL query — no explanation, no markdown, no backticks
2. Always use ROUND(value, 2) for any dollar amounts
3. Always use ORDER BY to sort results meaningfully
4. Use LIMIT 20 at most unless the question asks for all data
5. Column names are case-sensitive — use them exactly as shown in the schema
6. IMPORTANT: Order_Date is stored as TEXT in M/D/YYYY format (e.g. '11/8/2016').
   To filter by year use: SUBSTR(Order_Date, -4) = '2017'
   To extract month use: CAST(SUBSTR(Order_Date, 1, INSTR(Order_Date, '/') - 1) AS INTEGER)

User question: {question}

SQL query:"""

    try:
        #Sending the prompt to ChatGPT
        response = client.chat.completions.create(
            model = "gpt-4o",
            messages = [{"role":"user","content": prompt}],
            temperature = 0 #0 is more deterministic its good for coding problems
        )
        #Getting SQL query from CHATGPT response
        sql = response.choices[0].message.content.strip()
        print(f"\nGenerated SQL:\n{sql}\n")
        result_df = run_query(sql)
        #Lets explain our result in plain english to the user
        if not result_df.empty:
            explaination_prompt = f"""User asked: {question}
            We ran this SQL query: {sql}
            The Result was: {result_df.to_string}
            Write a clear 1-2 sentances explain our user the answer based on the question
            in plain english
            Important not: Be Specific Include Actual Numbers from the Result."""

            explaination_response = client.chat.completions.create(
                model = "gpt-4o",
                messages = [{"role":"user","content": explaination_prompt}],
                temperature = 0.3
            )
            answer = explaination_response.choices[0].message.content.strip()
        else:
            answer = "The Query returned has no result"
        
        return{
            "sql": sql,
            "result": result_df,
            "answer": answer,
            "error": ""
            }
    except Exception as e:
        return{
            "sql": "",
            "result": None,
            "answer": "",
            "error": str(e)
            }
    
# Test it with three real questions when we run this file directly
if __name__ == "__main__":

    questions = [
        "Which region had the highest total sales?",
        "What are the top 5 most profitable products?",
        "Which category has the most orders?"
    ]

    for question in questions:
        print("=" * 60)
        print(f"QUESTION: {question}")
        print("=" * 60)

        response = ask(question)

        if response["error"]:
            print(f"ERROR: {response['error']}")
        else:
            print(f"ANSWER: {response['answer']}")
            print(f"\nDATA:")
            print(response["result"].to_string())
        print()


    