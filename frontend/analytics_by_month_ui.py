import streamlit as st
from fastapi import HTTPException
import requests
import pandas as pd
import calendar

API_URL = "http://localhost:8000"


def analytics_by_month():
    response = requests.get(f"{API_URL}/analytics/monthly")
    if response.status_code == 200:
        expense = response.json()
    else:
        raise HTTPException("Didn't able to fetch data")
    
    st.subheader("Expense Breakdown By month")
    
    monthly_data = pd.DataFrame(expense)
    monthly_data["expense_month"] = monthly_data["expense_month"].apply(
        lambda m: calendar.month_name[int(m)]
    )


    monthly_data = monthly_data.set_index("expense_month")
    st.bar_chart(
        data = monthly_data,
        color="#4C78A8",
        height=400,
        width="stretch",
        x_label="month",
        y_label="expense"
    )
    monthly_data = monthly_data.map("{:.2f}".format)
    st.table(monthly_data, width="stretch")