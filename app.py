import streamlit as st
import pandas as pd
import os
import altair as alt
import matplotlib.pyplot as plt
from dotenv import load_dotenv
from utils import (
    fetch_articles_from_rss,
    fetch_articles_from_newsapi,
    analyze_sentiment,
    semantic_mapping
)

# ---------------- Load Environment Variables ----------------
load_dotenv()

# ---------------- Page Config ----------------
st.set_page_config(
    page_title="AI News Sentiment Tracker",
    layout="wide"
)

st.title("📰 AI News Sentiment Tracker")

# ---------------- Session State ----------------
if "df" not in st.session_state:
    st.session_state.df = None
if "data_loaded" not in st.session_state:
    st.session_state.data_loaded = False

# ---------------- Sidebar ----------------
with st.sidebar:
    st.header("Settings")

    source = st.selectbox("News Source", ["Google News (RSS)", "NewsAPI"])
    query = st.text_input("Search keyword", "technology")
    max_articles = st.slider("Max Articles", 5, 50, 20)

    api_key = ""
    if source == "NewsAPI":
        api_key = st.text_input(
            "Enter NewsAPI Key",
            value=os.getenv("NEWSAPI_KEY", ""),
            type="password"
        )

    fetch = st.button("Fetch & Analyze")

    st.markdown("---")
    st.subheader("📊 Chart Selection")
    chart_options = st.multiselect(
        "Select analysis (multiple allowed)",
        ["All", "Sentiment Distribution", "Compound Histogram", "Soul", "Materialism", "Actions"],
        default=["Sentiment Distribution"]
    )

    # -------- Semantic Interpretation Guide (TEXT ONLY) --------
    st.markdown("---")
    st.subheader("🧠 Semantic Interpretation Guide")

    st.markdown("""
**Positive Soul:** peace, trust, unity, love  
**Negative Soul:** pride, dominance, temptation  

**Positive Materialism:** sustainability, protection, longevity  
**Negative Materialism:** possession, exploitation, decay  

**Actions:** innovation, nurturing, transformation
""")

# ---------------- Fetch Data ----------------
if fetch:
    articles = (
        fetch_articles_from_rss(query, max_articles)
        if source == "Google News (RSS)"
        else fetch_articles_from_newsapi(query, max_articles, api_key)
    )

    if articles:
        df = pd.DataFrame(articles)
        sentiment_df = df["content"].apply(analyze_sentiment).apply(pd.Series)
        semantic_df = sentiment_df.apply(semantic_mapping, axis=1).apply(pd.Series)
        df = pd.concat([df, sentiment_df, semantic_df], axis=1)

        st.session_state.df = df
        st.session_state.data_loaded = True

# ---------------- Display ----------------
if st.session_state.data_loaded:
    df = st.session_state.df

    st.subheader("📄 Sentiment & Semantic Summary")
    st.dataframe(
        df[["title", "pos", "neu", "neg", "compound", "soul", "materialism", "actions"]],
        use_container_width=True
    )

    # ===== MAIN HEADER (not subheader) =====
    st.markdown("# 📊 Visual Analysis")

    show_all = "All" in chart_options

    # ---------- Sentiment Distribution ----------
    if show_all or "Sentiment Distribution" in chart_options:
        st.subheader("📊 Sentiment Distribution (Pos / Neu / Neg)")

        sent_df = (
            df[["pos", "neu", "neg"]]
            .mean()
            .reset_index()
            .rename(columns={"index": "Sentiment", 0: "Score"})
        )

        chart = (
            alt.Chart(sent_df)
            .mark_bar()
            .encode(
                x=alt.X("Sentiment:N", axis=alt.Axis(labelAngle=0)),
                y="Score:Q"
            )
            .properties(height=350)
        )

        st.altair_chart(chart, use_container_width=True)

    # ---------- Compound Histogram ----------
    if show_all or "Compound Histogram" in chart_options:
        st.subheader("Compound Sentiment Histogram")
        fig, ax = plt.subplots()
        ax.hist(df["compound"], bins=20, edgecolor="black")
        ax.set_xlabel("Compound Score")
        ax.set_ylabel("Number of Articles")
        st.pyplot(fig)

    # ---------- Soul ----------
    if show_all or "Soul" in chart_options:
        st.subheader("Soul Distribution")
        soul_df = df["soul"].value_counts().reset_index()
        soul_df.columns = ["Soul", "Count"]

        st.altair_chart(
            alt.Chart(soul_df)
            .mark_bar()
            .encode(
                x=alt.X("Soul:N", axis=alt.Axis(labelAngle=0)),
                y="Count:Q"
            )
            .properties(height=300),
            use_container_width=True
        )

    # ---------- Materialism ----------
    if show_all or "Materialism" in chart_options:
        st.subheader("Materialism Distribution")
        mat_df = df["materialism"].value_counts().reset_index()
        mat_df.columns = ["Materialism", "Count"]

        st.altair_chart(
            alt.Chart(mat_df)
            .mark_bar()
            .encode(
                x=alt.X("Materialism:N", axis=alt.Axis(labelAngle=0)),
                y="Count:Q"
            )
            .properties(height=300),
            use_container_width=True
        )

    # ---------- Actions ----------
    if show_all or "Actions" in chart_options:
        st.subheader("Actions Distribution")
        act_df = df["actions"].value_counts().reset_index()
        act_df.columns = ["Actions", "Count"]

        st.altair_chart(
            alt.Chart(act_df)
            .mark_bar()
            .encode(
                x=alt.X("Actions:N", axis=alt.Axis(labelAngle=0)),
                y="Count:Q"
            )
            .properties(height=300),
            use_container_width=True
        )

    # ---------- Download ----------
    st.download_button(
        "⬇️ Download Results as CSV",
        df.to_csv(index=False),
        "news_sentiment_analysis.csv",
        "text/csv"
    )
