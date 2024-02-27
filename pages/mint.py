import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection


from datetime import datetime

st.title("📗 Mint")

url = "https://docs.google.com/spreadsheets/d/1n-hcvcfR4yMxqcolyOq2rBauGH1nFtCkWYYZgUgyEDs/edit?usp=sharing"

conn = st.connection("gsheets", type=GSheetsConnection)

# Read data from Google Sheets
google_data = conn.read(spreadsheet=url, usecols=[0, 1, 2, 3, 4, 5])


pandas_data = pd.DataFrame(google_data)

pandas_data['DATE'] = pd.to_datetime(pandas_data['DATE']).dt.date


col1, col2 = st.columns(2)

# Add date inputs to the columns
with col1:
    start_date = st.date_input("Start date")

with col2:
    end_date = st.date_input("End date")

categories = st.multiselect("Select Categories", pandas_data['CATEGORY'].unique())

formatted_start = start_date.strftime("%B %d, %Y")
formatted_end = end_date.strftime("%B %d, %Y")

st.subheader("🗓 " + formatted_start + " to " + formatted_end)
if not categories:
    st.subheader("🗂 All Categories")
else:
    subheader_text = " + ".join(categories)
    st.subheader("🗂 Categories: " + subheader_text)

# Convert date inputs to datetime objects
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
    st.write(filtered_df)

else:
    st.error("End date must be after start date.")
