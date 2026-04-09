# 📊 NL-to-SQL Sales Analytics Chatbot

A full-stack AI-powered analytics chatbot that converts plain English questions into SQL queries, runs them against a real sales database, and returns answers with interactive charts.

**Live Demo:** [your-app-url-here](https://hrutvikk-nl-to-sql-chatbot.streamlit.app)

---

## What it does

You type a question like _"Which region had the highest sales in 2017?"_ and the app:

1. Sends your question + database schema to GPT-4o
2. GPT-4o writes the SQL query
3. The app runs the query against a real SQLite database
4. Results are displayed as a table, chart, and plain English answer

---

## Screenshot

> _Add a screenshot of your app here after deployment_

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| AI / LLM | OpenAI GPT-4o |
| Database | SQLite |
| Data processing | Python, Pandas, SQLAlchemy |
| Charts | Plotly |
| Deployment | Streamlit Cloud |

---

## Features

- **Natural language to SQL** — ask any business question in plain English
- **Auto chart generation** — bar and line charts generated automatically based on result shape
- **SQL transparency** — see the exact SQL query GPT-4o generated for every question
- **Query history** — review all previous questions and answers in the session
- **Suggested prompts** — one-click example questions to get started
- **KPI dashboard** — live metrics showing query count, result rows, and engine status
- **Error handling** — graceful error messages when queries fail

---

## Dataset

Uses the [Superstore Sales Dataset](https://www.kaggle.com/datasets/vivek468/superstore-dataset-final) from Kaggle.

- 9,994 rows, 21 columns
- Covers orders from 2014–2017
- Key columns: `Region`, `Category`, `Sub_Category`, `Sales`, `Profit`, `Discount`, `Order_Date`

---

## Project Structure

```
nl-to-sql-chatbot/
├── app.py              # Streamlit UI — main entry point
├── chain.py            # GPT-4o integration — NL to SQL to answer
├── query_runner.py     # SQL execution layer — runs queries on SQLite
├── database.py         # Database setup — loads CSV into SQLite
├── setup_db.py         # Auto-setup — creates DB on first run
├── requirements.txt    # Python dependencies
├── .env                # API key (local only, never committed)
├── .gitignore          # Ignores .env and generated files
└── data/
    └── superstore.csv  # Source dataset
```

---

## How it works

### 1. Database layer
`database.py` reads the CSV using Pandas, cleans column names, and loads all 9,994 rows into a SQLite database using SQLAlchemy. SQLite was chosen because it requires no server setup and deploys as a single file.

### 2. Query runner
`query_runner.py` exposes three functions:
- `run_query(sql)` — executes any SQL string and returns a Pandas DataFrame
- `get_schema()` — returns column names and types for the GPT-4o prompt
- `preview_table()` — returns sample rows for debugging

### 3. AI chain
`chain.py` builds a prompt that includes the full database schema and the user's question, sends it to GPT-4o with `temperature=0` for deterministic SQL output, runs the result, then asks GPT-4o to explain the answer in plain English.

### 4. Streamlit UI
`app.py` renders the full dashboard — hero section, KPI cards, question input, suggested prompts, results tabs, and query history — all in a custom dark theme.

---

## Running locally

### Prerequisites
- Python 3.11+
- OpenAI API key with billing enabled

### Setup

```bash
# Clone the repo
git clone https://github.com/hrutvikk/nl-to-sql-chatbot.git
cd nl-to-sql-chatbot

# Install dependencies
pip install -r requirements.txt

# Add your OpenAI API key
echo 'OPENAI_API_KEY=sk-your-key-here' > .env

# Run the app
streamlit run app.py
```

The app will open at `http://localhost:8501`.

---

## Example questions to try

```
Which region had the highest total sales?
What are the top 5 most profitable products?
Which sub-categories are losing money?
Show me monthly sales trend for 2017
Which state has the highest average discount?
Who are the top 10 customers by total purchases?
What is the total profit for each category in the East region?
```

---

## Deployment

Deployed on [Streamlit Cloud](https://streamlit.io/cloud) with the OpenAI API key stored securely as an environment secret — never committed to the repository.

---

## Author

**Hrutvik** — Masters in Information Systems, University of Florida

- GitHub: [github.com/hrutvikk](https://github.com/hrutvikk)

---

## License

MIT License — free to use and modify.
