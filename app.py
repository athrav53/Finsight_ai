
from modules.statement_upload import show_statement_upload
import streamlit as st
import pandas as pd
import plotly.express as px

from analytics.queries import get_users, get_date_range, get_dashboard_data

st.set_page_config(
    page_title="FinSight AI",
    page_icon="💰",
    layout="wide"
)

st.title("💰 FinSight AI")
st.caption("Interactive Bank Statement Analytics Dashboard")

# Sidebar filters
st.sidebar.header("Filters")

users = [row[0] for row in get_users()]

selected_user = st.sidebar.selectbox(
    "Select User",
    ["All Users"] + users
)

min_date, max_date = get_date_range()

if min_date is None:
    st.warning("No transactions available in database.")
    st.stop()

selected_dates = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

if len(selected_dates) != 2:
    st.info("Please select both start and end dates.")
    st.stop()

start_date, end_date = selected_dates

user_id = None if selected_user == "All Users" else selected_user

df = get_dashboard_data(user_id, start_date, end_date)

if df.empty:
    st.warning("No transactions found for selected filters.")
    st.stop()

# KPI calculations
debits = df[df["Type"] == "Debit"]
credits = df[df["Type"] == "Credit"]

total_spending = debits["Amount"].sum()
total_income = credits["Amount"].sum()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Transactions", len(df))
col2.metric("Total Spending", f"₹{total_spending:,.2f}")
col3.metric("Total Income", f"₹{total_income:,.2f}")
col4.metric("Net Cash Flow", f"₹{total_income-total_spending:,.2f}")

st.divider()

left, right = st.columns(2)

with left:
    st.subheader("Category-wise Spending")

    category_df = (
        debits.assign(
            Category=debits["Category"].fillna("Uncategorized")
        )
        .groupby("Category", as_index=False)["Amount"]
        .sum()
        .sort_values("Amount", ascending=False)
    )

    if not category_df.empty:
        fig = px.bar(
            category_df,
            x="Category",
            y="Amount",
            color="Category"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No debit transactions.")

with right:
    st.subheader("Monthly Spending")

    monthly_df = debits.copy()

    if not monthly_df.empty:
        monthly_df["Month"] = monthly_df["Date"].dt.to_period("M").astype(str)

        monthly_df = (
            monthly_df.groupby("Month", as_index=False)["Amount"]
            .sum()
        )

        fig = px.line(
            monthly_df,
            x="Month",
            y="Amount",
            markers=True
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No monthly spending data.")

st.divider()

st.subheader("Top 10 Merchants")

merchant_df = (
    debits.assign(
        Merchant=debits["Merchant"].fillna("Unknown")
    )
    .groupby("Merchant", as_index=False)["Amount"]
    .sum()
    .sort_values("Amount", ascending=False)
    .head(10)
)

if not merchant_df.empty:
    fig = px.bar(
        merchant_df,
        x="Amount",
        y="Merchant",
        orientation="h"
    )
    st.plotly_chart(fig, use_container_width=True)

st.divider()

st.subheader("Transaction History")

search = st.text_input("Search transactions")

filtered_df = df.copy()

if search:
    mask = (
        filtered_df.astype(str)
        .apply(
            lambda col: col.str.contains(
                search, case=False, regex=False, na=False
            )
        )
        .any(axis=1)
    )
    filtered_df = filtered_df[mask]

st.dataframe(
    filtered_df,
    use_container_width=True,
    hide_index=True
)

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Filtered CSV",
    data=csv,
    file_name="finsight_transactions.csv",
    mime="text/csv"
)
st.divider()
show_statement_upload()
