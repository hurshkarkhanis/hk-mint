import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

# Setting up the Streamlit app title
st.title("📗 Pocketbook AI: Modern Personal Finance")

# Google Sheets URL
url = "https://docs.google.com/spreadsheets/d/1n-hcvcfR4yMxqcolyOq2rBauGH1nFtCkWYYZgUgyEDs/edit?usp=sharing"

# Establishing connection to Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# Read data from Google Sheets
google_data = conn.read(spreadsheet=url, usecols=[0, 1, 2, 3, 4, 5])
pandas_data = pd.DataFrame(google_data)

# Convert 'DATE' column to datetime objects
pandas_data['DATE'] = pd.to_datetime(pandas_data['DATE']).dt.date

# Creating two columns for date inputs
col1, col2 = st.columns(2)

# Add date inputs to the columns
with col1:
    start_date = st.date_input("Start date", datetime(2024, 1, 1))

with col2:
    end_date = st.date_input("End date", datetime.now().date())

# Selecting categories
categories = st.multiselect("Select Categories", pandas_data['CATEGORY'].unique(), placeholder="Default: all")

# Formatting date inputs
formatted_start = start_date.strftime("%B %d, %Y")
formatted_end = end_date.strftime("%B %d, %Y")

# Displaying date range and selected categories
st.subheader("🗓 " + formatted_start + " to " + formatted_end)
if not categories:
    st.subheader("🗂 All Categories")
else:
    subheader_text = " + ".join(categories)
    st.subheader("🗂 Categories: " + subheader_text)

# Filtering data based on date range and selected categories
start_datetime = datetime.combine(start_date, datetime.min.time())
end_datetime = datetime.combine(end_date, datetime.max.time())

if start_datetime <= end_datetime:
    if not categories:
        filtered_df = pandas_data[(pandas_data['DATE'] >= start_datetime.date()) & 
                              (pandas_data['DATE'] <= end_datetime.date())]
    else:
        filtered_df = pandas_data[(pandas_data['DATE'] >= start_datetime.date()) & 
                                (pandas_data['DATE'] <= end_datetime.date()) & 
                                (pandas_data['CATEGORY'].isin(categories))]
else:
    st.error("End date must be after start date.")

# Calculating spending metrics
total_spend = sum(filtered_df['PRICE'])
median_spend = filtered_df['PRICE'].median()
min_spend = min(filtered_df['PRICE'])
max_spend = max(filtered_df['PRICE'])

# Formatting spending metrics as dollars
total_spend_formatted = "${:,.2f}".format(total_spend)
median_spend_formatted = "${:,.2f}".format(median_spend)
min_spend_formatted = "${:,.2f}".format(min_spend)
max_spend_formatted = "${:,.2f}".format(max_spend)

# Displaying spending metrics
column_names = ["Min Spend", "Median Spend", "Max Spend", "Total Spend"]
formatted_values = [min_spend_formatted, median_spend_formatted, max_spend_formatted, total_spend_formatted]

for i, (col, value) in enumerate(zip(st.columns(4), formatted_values)):
    with col:
        st.metric(column_names[i], value)

# Displaying spending distribution by category using a bar chart
st.subheader("Spending Distribution")
category_spend = filtered_df.groupby('CATEGORY')['PRICE'].sum()
st.bar_chart(category_spend)
