import pandas as pd
import streamlit as st


st.title("💬 Upload")


st.header("📝 Query any CSV file using plain English")

uploaded_file = st.file_uploader("", type=['csv'])

if uploaded_file is not None:
    try:
        pandas_data = pd.read_csv(uploaded_file)
        
        # Expander to display raw data
        with st.expander("View File"):
            st.write(pandas_data)

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
            response = agent.run(question)
            return response

        # User input for the question
        user_question = st.text_input("Enter your question:", "...")

        # Submit button to trigger Langchain interaction
        if st.button("Submit"):
            if user_question:
                langchain_response = interact_with_langchain(user_question)
                st.write(langchain_response)
            else:
                st.warning("Please enter a question.")
            
    except ValueError as ve:
        st.error("An error occurred: Please make sure the uploaded file is not empty or in the correct CSV format.")
