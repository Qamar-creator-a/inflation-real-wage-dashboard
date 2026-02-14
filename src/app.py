import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

from src.real_wage import to_real_income, inflation_yoy

st.title("Inflation Tracker + Real Wage Dashboard")

st.write("Upload a CSV with columns: date, income (monthly). date format like 2024-01-01.")

uploaded = st.file_uploader("Income CSV", type=["csv"])

# Placeholder CPI input for now (you’ll replace with live CPI fetch)
st.subheader("CPI (demo placeholder)")
idx = pd.date_range("2023-01-01", periods=36, freq="MS")
cpi = pd.Series(300 + (pd.Series(range(36)) * 0.7).values, index=idx)  # fake CPI trend

base_date = st.selectbox("Choose base month", options=list(cpi.index), format_func=lambda d: d.strftime("%Y-%m"))

if uploaded:
    df = pd.read_csv(uploaded)
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")
    income = pd.Series(df["income"].values, index=df["date"])

    real = to_real_income(income, cpi, base_date)
    yoy = inflation_yoy(cpi)

    st.subheader("Charts")

    fig1 = plt.figure()
    plt.plot(cpi.index, cpi.values)
    plt.title("CPI (Index)")
    st.pyplot(fig1)

    fig2 = plt.figure()
    plt.plot(income.index, income.values, label="Nominal Income")
    plt.plot(real.index, real.values, label="Real Income")
    plt.legend()
    plt.title("Nominal vs Real Income")
    st.pyplot(fig2)

    st.subheader("Inflation (YoY)")
    fig3 = plt.figure()
    plt.plot(yoy.index, yoy.values)
    plt.title("YoY Inflation Rate")
    st.pyplot(fig3)
else:
    st.info("Upload an income CSV to see your real wage chart.")
