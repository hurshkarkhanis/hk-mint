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

# AI Interaction Section
st.subheader("Ask PocketBook:")

# Importing necessary libraries
import os
from dotenv import load_dotenv, find_dotenv

# Loading API key from environment variables
load_dotenv(find_dotenv())
my_key = os.getenv('OPEN_AI_API_KEY')

# Importing Langchain-related modules
from langchain_community.chat_models import ChatOpenAI
from langchain_experimental.agents import create_pandas_dataframe_agent

# Creating Langchain agent with verbose output
chat = ChatOpenAI(model_name='gpt-3.5-turbo', 
                  temperature=0, 
                  openai_api_key=my_key
                  )
agent = create_pandas_dataframe_agent(chat, pandas_data, verbose=True)

# Function to interact with Langchain agent
def interact_with_langchain(question):
    response = agent.run(question)
    return response

# User input for the question
user_question = st.text_input("Enter your question:", "...")
question_asked = False

# Submit button to trigger Langchain interaction
if st.button("Submit"):
    if user_question:
        question_asked = True
        langchain_response = interact_with_langchain(user_question)
        st.write(langchain_response)
    else:
        st.warning("Please enter a question.")

# Show the "Clear" button only if a question has been asked and answered
if question_asked:
    if st.button("Clear"):
        user_question = ""
        langchain_response = ""
        st.text_input("Enter your question:", value="Enter your question:")
        st.write("()()")
        st.write(langchain_response)

# Expander to display raw data
with st.expander("See Raw Data"):
    st.write(pandas_data)