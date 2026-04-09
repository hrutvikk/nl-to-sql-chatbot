# app.py
# Modernized Streamlit UI for the NL-to-SQL chatbot.

import streamlit as st
import pandas as pd
import plotly.express as px
from setup_db import ensure_db_exists
from chain import ask

ensure_db_exists()

# ── Page config ──────────────────────────────────────────
st.set_page_config(
    page_title="Sales Analytics Chatbot",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Session state ────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []

if "prefill" not in st.session_state:
    st.session_state.prefill = ""

if "last_response" not in st.session_state:
    st.session_state.last_response = None

# ── Custom CSS ───────────────────────────────────────────
st.markdown("""
<style>
    .stApp {
        background:
            radial-gradient(circle at top left, rgba(93, 95, 239, 0.10), transparent 28%),
            radial-gradient(circle at top right, rgba(0, 200, 255, 0.08), transparent 25%),
            linear-gradient(180deg, #0b1020 0%, #111827 100%);
        color: #e5e7eb;
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1500px;
    }
    h1, h2, h3, h4, h5, h6 { color: #f9fafb !important; letter-spacing: -0.02em; }
    p, div, label, span { color: #d1d5db; }
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #111827 100%);
        border-right: 1px solid rgba(255,255,255,0.06);
    }
    .sidebar-brand {
        padding: 1rem 0.5rem 1.25rem 0.5rem;
        margin-bottom: 1rem;
        border-bottom: 1px solid rgba(255,255,255,0.08);
    }
    .brand-badge {
        display: inline-block;
        padding: 0.35rem 0.7rem;
        border-radius: 999px;
        background: linear-gradient(90deg, #6366f1, #06b6d4);
        color: white;
        font-size: 0.75rem;
        font-weight: 700;
        margin-bottom: 0.75rem;
        box-shadow: 0 8px 24px rgba(99,102,241,0.35);
    }
    .brand-title { font-size: 1.25rem; font-weight: 800; color: #ffffff; margin: 0; }
    .brand-subtitle { font-size: 0.9rem; color: #94a3b8; margin-top: 0.25rem; line-height: 1.5; }
    .hero-card {
        background: linear-gradient(135deg, rgba(99,102,241,0.18), rgba(6,182,212,0.10));
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 24px;
        padding: 1.6rem 1.6rem 1.3rem 1.6rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.20);
        margin-bottom: 1rem;
    }
    .hero-top {
        display: inline-block;
        padding: 0.35rem 0.75rem;
        border-radius: 999px;
        background: rgba(255,255,255,0.08);
        border: 1px solid rgba(255,255,255,0.08);
        font-size: 0.78rem;
        font-weight: 600;
        color: #cbd5e1;
        margin-bottom: 0.9rem;
    }
    .hero-title { font-size: 2.1rem; font-weight: 800; color: #ffffff; line-height: 1.15; margin-bottom: 0.45rem; }
    .hero-subtitle { font-size: 1rem; color: #cbd5e1; line-height: 1.7; max-width: 900px; }
    .metric-card {
        background: rgba(17, 24, 39, 0.82);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 20px;
        padding: 1rem 1.1rem;
        box-shadow: 0 8px 25px rgba(0,0,0,0.18);
        transition: all 0.25s ease;
        min-height: 110px;
    }
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 14px 32px rgba(0,0,0,0.24);
        border-color: rgba(99,102,241,0.35);
    }
    .metric-label { color: #94a3b8; font-size: 0.82rem; font-weight: 600; margin-bottom: 0.55rem; text-transform: uppercase; letter-spacing: 0.06em; }
    .metric-value { color: white; font-size: 1.8rem; font-weight: 800; line-height: 1.1; margin-bottom: 0.25rem; }
    .metric-help { color: #cbd5e1; font-size: 0.88rem; }
    .panel-card {
        background: rgba(17, 24, 39, 0.82);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 22px;
        padding: 1.15rem 1.15rem 1rem 1.15rem;
        box-shadow: 0 10px 28px rgba(0,0,0,0.18);
        margin-bottom: 1rem;
    }
    .panel-title { font-size: 1.05rem; font-weight: 700; color: #ffffff; margin-bottom: 0.35rem; }
    .panel-subtitle { font-size: 0.92rem; color: #94a3b8; margin-bottom: 0.9rem; }
    .muted-text { color: #94a3b8; font-size: 0.92rem; }
    div.stButton > button {
        border-radius: 14px !important;
        border: 1px solid rgba(255,255,255,0.10) !important;
        padding: 0.7rem 1rem !important;
        font-weight: 600 !important;
        transition: all 0.25s ease !important;
        box-shadow: 0 6px 18px rgba(0,0,0,0.12) !important;
    }
    div.stButton > button:hover {
        transform: translateY(-1px);
        border-color: rgba(99,102,241,0.45) !important;
        box-shadow: 0 12px 24px rgba(0,0,0,0.18) !important;
    }
    div[data-baseweb="input"] > div {
        background: rgba(15, 23, 42, 0.9) !important;
        border-radius: 16px !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
    }
    div[data-baseweb="input"] input { color: #f9fafb !important; }
    button[data-baseweb="tab"] { border-radius: 12px !important; padding: 0.6rem 0.9rem !important; }
    .streamlit-expanderHeader { font-weight: 700; color: #f8fafc; }
    hr { border-color: rgba(255,255,255,0.08); }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ──────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <div class="brand-badge">AI ANALYTICS</div>
        <div class="brand-title">Sales Analytics</div>
        <div class="brand-subtitle">
            Natural language to SQL insights for your Superstore data.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Navigation")
    nav = st.radio("Go to", ["Ask Query", "History"], label_visibility="collapsed")

    st.markdown("---")
    st.markdown("### Quick Stats")
    total_queries = len(st.session_state.history)
    last_question = (
        st.session_state.history[-1]["question"]
        if st.session_state.history else "No queries yet"
    )
    st.metric("Total Queries", total_queries)
    st.metric("Example Prompts", 5)
    st.caption(f"Last query: {last_question[:45]}{'...' if len(last_question) > 45 else ''}")

# ── Header / Hero ────────────────────────────────────────
st.markdown("""
<div class="hero-card">
    <div class="hero-top">Modern AI SQL Dashboard</div>
    <div class="hero-title">Ask your sales data in plain English</div>
    <div class="hero-subtitle">
        Turn business questions into SQL, explore tabular results, and visualize patterns instantly
        with a cleaner, premium analytics experience.
    </div>
</div>
""", unsafe_allow_html=True)

# ── KPI row ──────────────────────────────────────────────
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Queries Asked</div>
        <div class="metric-value">{len(st.session_state.history)}</div>
        <div class="metric-help">Session activity</div>
    </div>
    """, unsafe_allow_html=True)

with kpi2:
    last_sql_status = "Ready" if st.session_state.last_response else "Waiting"
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">SQL Engine</div>
        <div class="metric-value">{last_sql_status}</div>
        <div class="metric-help">Generated on demand</div>
    </div>
    """, unsafe_allow_html=True)

with kpi3:
    last_rows = 0
    if st.session_state.last_response and isinstance(
        st.session_state.last_response.get("result"), pd.DataFrame
    ):
        last_rows = len(st.session_state.last_response["result"])
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Last Result Rows</div>
        <div class="metric-value">{last_rows}</div>
        <div class="metric-help">Most recent query output</div>
    </div>
    """, unsafe_allow_html=True)

with kpi4:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">Data Source</div>
        <div class="metric-value">Superstore</div>
        <div class="metric-help">Sales dataset</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("")

# ── Ask Query View ───────────────────────────────────────
if nav == "Ask Query":
    left, right = st.columns([1.35, 1], gap="large")

    with left:
        st.markdown("""
        <div class="panel-card">
            <div class="panel-title">Ask a question</div>
            <div class="panel-subtitle">
                Use one of the example prompts or type your own question below.
            </div>
        </div>
        """, unsafe_allow_html=True)

        examples = [
            "Which region had the highest total sales?",
            "What are the top 5 most profitable products?",
            "Which category has the most orders?",
            "Show me monthly sales trend for 2017",
            "Which state has the highest average discount?"
        ]

        st.markdown("#### Suggested prompts")
        ex_cols = st.columns(2, gap="small")
        for i, example in enumerate(examples):
            with ex_cols[i % 2]:
                # FIX: write to 'prefill' not 'question' to avoid key conflict
                if st.button(example, key=f"example_{i}", use_container_width=True):
                    st.session_state.prefill = example
                    st.rerun()

        st.markdown("")

        # FIX: use 'prefill' as the value, bind widget to its own key 'question_input'
        question = st.text_input(
            label="Your question",
            value=st.session_state.prefill,
            placeholder="e.g. Which city had the lowest profit last year?",
            key="question_input"
        )

        ask_col, info_col = st.columns([1, 2.2])
        with ask_col:
            run = st.button("Ask", type="primary", use_container_width=True)
        with info_col:
            st.markdown(
                "<div class='muted-text' style='padding-top: 0.65rem;'>"
                "Tip: questions with trends, rankings, regions, categories work well."
                "</div>",
                unsafe_allow_html=True
            )

    with right:
        st.markdown("""
        <div class="panel-card">
            <div class="panel-title">How it works</div>
            <div class="panel-subtitle">
                The app converts your question into SQL, runs it, and displays
                the answer, table, and chart.
            </div>
        </div>
        """, unsafe_allow_html=True)
        info_a, info_b = st.columns(2)
        with info_a:
            st.info("**Step 1**\n\nWrite your question in plain English.")
        with info_b:
            st.info("**Step 2**\n\nReview the answer, SQL, results, and chart.")

    # ── Main logic ────────────────────────────────────────
    if run and question.strip():
        with st.spinner("Thinking..."):
            response = ask(question)

        st.session_state.last_response = response
        st.session_state.prefill = ""  # clear prefill after running

        if response["error"]:
            st.error(f"Something went wrong: {response['error']}")
        else:
            df = response["result"]

            st.session_state.history.append({
                "question": question,
                "answer": response["answer"],
                "sql": response["sql"]
            })

            st.markdown("### Results Overview")
            answer_col, summary_col = st.columns([2.2, 1], gap="large")

            with answer_col:
                st.success(response["answer"])

            with summary_col:
                result_count = len(df) if isinstance(df, pd.DataFrame) else 0
                sql_lines = len(response["sql"].splitlines()) if response.get("sql") else 0
                st.metric("Rows Returned", result_count)
                st.metric("SQL Lines", sql_lines)

            tab_results, tab_chart, tab_sql = st.tabs(["Results", "Chart", "Generated SQL"])

            with tab_results:
                st.markdown("""
                <div class="panel-card">
                    <div class="panel-title">Query results</div>
                    <div class="panel-subtitle">Structured output from your data source.</div>
                </div>
                """, unsafe_allow_html=True)
                st.dataframe(df, use_container_width=True, height=420)

            with tab_chart:
                st.markdown("""
                <div class="panel-card">
                    <div class="panel-title">Auto visualization</div>
                    <div class="panel-subtitle">Chart generated when output shape is suitable.</div>
                </div>
                """, unsafe_allow_html=True)

                chart_rendered = False
                if df is not None and len(df.columns) == 2:
                    col_x = df.columns[0]
                    col_y = df.columns[1]
                    if pd.api.types.is_numeric_dtype(df[col_y]):
                        if len(df) <= 10:
                            fig = px.bar(
                                df, x=col_x, y=col_y, title=question,
                                color=col_x,
                                color_discrete_sequence=px.colors.qualitative.Set2
                            )
                        else:
                            fig = px.line(
                                df, x=col_x, y=col_y, title=question, markers=True
                            )
                        fig.update_layout(
                            showlegend=False,
                            paper_bgcolor="rgba(0,0,0,0)",
                            plot_bgcolor="rgba(0,0,0,0)",
                            margin=dict(l=10, r=10, t=55, b=10),
                            font=dict(color="#e5e7eb"),
                            title_font=dict(size=18),
                        )
                        fig.update_xaxes(showgrid=False)
                        fig.update_yaxes(gridcolor="rgba(255,255,255,0.10)")
                        st.plotly_chart(fig, use_container_width=True)
                        chart_rendered = True

                if not chart_rendered:
                    st.warning(
                        "No chart available. Charts appear when the query returns "
                        "exactly 2 columns and the second is numeric."
                    )

            with tab_sql:
                st.markdown("""
                <div class="panel-card">
                    <div class="panel-title">Generated SQL</div>
                    <div class="panel-subtitle">Review the query produced from your prompt.</div>
                </div>
                """, unsafe_allow_html=True)
                st.code(response["sql"], language="sql")

# ── History View ─────────────────────────────────────────
elif nav == "History":
    st.markdown("""
    <div class="panel-card">
        <div class="panel-title">Query History</div>
        <div class="panel-subtitle">
            Review previous questions, answers, and SQL from this session.
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.history:
        hist_k1, hist_k2, hist_k3 = st.columns(3)
        with hist_k1:
            st.metric("Total Saved Queries", len(st.session_state.history))
        with hist_k2:
            st.metric("Most Recent", "Available")
        with hist_k3:
            st.metric("Session State", "Active")

        st.markdown("")
        for i, item in enumerate(reversed(st.session_state.history), start=1):
            with st.expander(f"Q{i}: {item['question']}"):
                st.write(item["answer"])
                st.code(item["sql"], language="sql")
    else:
        st.info("No query history yet. Ask your first question from the dashboard.")