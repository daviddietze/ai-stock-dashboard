import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="AI Stock Dashboard", layout="wide")

SECTORS = {
    "Technology": ["MSFT", "AAPL", "NVDA", "AVGO"],
    "Healthcare": ["LLY", "UNH", "ISRG"],
    "Financials": ["JPM", "GS"],
    "Consumer": ["AMZN", "COST"],
}

def get_data(ticker):
    t = yf.Ticker(ticker)
    info = t.info
    hist = t.history(period="6mo")
    return {
        "ticker": ticker,
        "price": info.get("currentPrice"),
        "revenue_growth": info.get("revenueGrowth"),
        "profit_margin": info.get("profitMargins"),
        "beta": info.get("beta"),
        "perf_6m": hist["Close"].pct_change().sum()
    }

def score_stock(data):
    score = 0
    if data["revenue_growth"]:
        score += data["revenue_growth"] * 50
    if data["perf_6m"]:
        score += data["perf_6m"] * 30
    if data["profit_margin"]:
        score += data["profit_margin"] * 20
    return round(score, 2)

def explain(data):
    reasons = []
    if data["revenue_growth"] and data["revenue_growth"] > 0.15:
        reasons.append("strong growth")
    if data["perf_6m"] and data["perf_6m"] > 0.2:
        reasons.append("good momentum")
    if data["profit_margin"] and data["profit_margin"] > 0.15:
        reasons.append("solid margins")
    return ", ".join(reasons)

st.title("AI Stock Picker")

if st.button("Run Model"):
    results = []
    for sector, stocks in SECTORS.items():
        for ticker in stocks:
            try:
                data = get_data(ticker)
                score = score_stock(data)
                data["score"] = score
                data["sector"] = sector
                data["reason"] = explain(data)
                results.append(data)
            except:
                pass

    df = pd.DataFrame(results)

    if not df.empty:
        df = df.sort_values("score", ascending=False).head(5)

        st.subheader("Top Picks")

        for _, row in df.iterrows():
            st.write(f"{row['ticker']} ({row['sector']})")
            st.write(f"Score: {row['score']}")
            st.write(f"Why: {row['reason']}")
            st.write("---")
