import pandas as pd
import streamlit as st
from datetime import datetime

st.title("🙋🏻‍♂️ Bring Your Own Data (BYOD)")

st.subheader("😎 Upload your financial data for AI powered insights")



with st.expander("⚠️ Guidelines for File Upload"):
        st.markdown('''
                    1. File MUST be CSV format
                    2. File MUST contain these columns at least (case sensitive)
                        * DATE
                        * CATEGORY
                        * PRICE
                    ''')


uploaded_file = st.file_uploader("⬇️ Upload Here", type=['csv'])

if uploaded_file is not None:

    try:

        pandas_data = pd.read_csv(uploaded_file)

        with st.expander("View Uploaded Data"):
            st.write(pandas_data)

        # Convert 'DATE' column to datetime objects
        pandas_data['DATE'] = pd.to_datetime(pandas_data['DATE']).dt.date

        # Assuming you have loaded your DataFrame into df
        # Compute min and max dates
        min_date = pandas_data['DATE'].min()
        max_date = pandas_data['DATE'].max()

    # Set up your Streamlit layout
        col1, col2 = st.columns(2)

        # Date inputs with initial values set to min and max dates
        with col1:
            start_date = st.date_input("Start date", min_date)

        with col2:
            end_date = st.date_input("End date", max_date)

        # Selecting categories
        categories = st.multiselect("Filter by Category", pandas_data['CATEGORY'].unique(), placeholder="Default: all")

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

        #####################################################################################

        # AI Interaction Section
        st.header("📝 Query financial data in plain English")
        st.subheader("😎 No need for SQL or Python data skills")


        # Importing necessary libraries
        import os
        from dotenv import load_dotenv, find_dotenv

        # Loading API key from environment variables
        load_dotenv(find_dotenv())
        my_key = os.getenv('OPEN_AI_API_KEY')

        # Importing Langchain-related modules
        from langchain_openai import ChatOpenAI
        from langchain_experimental.agents import create_pandas_dataframe_agent

        # Creating Langchain agent with verbose output
        chat = ChatOpenAI(model_name='gpt-3.5-turbo', 
                        temperature=0, 
                        openai_api_key=my_key
                        )
        agent = create_pandas_dataframe_agent(chat, pandas_data, verbose=True)

        # Function to interact with Langchain agent
        def interact_with_langchain(question):
            response = agent.invoke(question)
            return response['output']

        # User input for the question
        user_question = st.text_input("Enter your question:")
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
            if st.button("Clear Output"):
                user_question = ""
                langchain_response = ""
                st.text_input("Enter your question:", value="Enter your question:")
                st.write("()()")
                st.write(langchain_response)

    except ValueError as ve:
        st.error("An error occurred: Please make sure the uploaded file is not empty or in the correct CSV format.")




