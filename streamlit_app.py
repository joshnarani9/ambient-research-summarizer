import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

DB_PATH = "research_summaries.db"  # adjust if your DB is elsewhere

# ------------------------------------------------------------
# Load summaries from database
# ------------------------------------------------------------
def load_summaries():
    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query("SELECT * FROM summaries ORDER BY created_at DESC", conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"⚠️ Unable to load summaries: {e}")
        return pd.DataFrame(columns=["summary", "link", "created_at", "category"])

# ------------------------------------------------------------
# Streamlit UI
# ------------------------------------------------------------
st.set_page_config(page_title="Ambient Research Summaries", layout="wide")
st.title("🧠 Ambient Research Summaries Dashboard")

st.caption("Automatically generated summaries of AI & tech research, powered by Gemini and sent via Slack.")

# Category filter (optional)
df = load_summaries()

if not df.empty:
    # Ensure created_at is readable
    if "created_at" in df.columns:
        df["created_at"] = pd.to_datetime(df["created_at"])

    categories = sorted(df["category"].dropna().unique()) if "category" in df.columns else []
    selected_category = st.sidebar.selectbox("Filter by Category", ["All"] + categories)

    if selected_category != "All" and "category" in df.columns:
        df = df[df["category"] == selected_category]

    # Display summaries
    for _, row in df.iterrows():
        st.markdown(f"### 🧩 {row['summary']}")
        st.write(f"🔗 [Read more]({row['link']})")
        st.caption(f"🕒 {row['created_at']}")
        st.markdown("---")
else:
    st.info("No summaries found yet. Ambient agent might still be fetching updates...")

st.sidebar.markdown("---")
st.sidebar.info("💡 Tip: Keep this page open to view latest AI/tech research summaries fetched automatically every few minutes.")
