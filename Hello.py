# Import necessary libraries
import streamlit as st
from streamlit.logger import get_logger

# Get logger
LOGGER = get_logger(__name__)

# Function to run the Streamlit app
def run():
    # Set page configuration
    st.set_page_config(
        page_title="Pocketbook AI",
        page_icon="📗",
    )

    # Write main header
    st.write("# 📗 Welcome to Pocketbook AI")

    # Write introduction
    st.markdown(
        """
        **👨🏻‍💻 I built Pocketbook AI to give myself a personal finance tool** after
        [Mint shut down](https://www.cnbc.com/select/mint-app-shutting-down-what-users-should-do/)
        at the end of 2023. 

        🔄 **This tool uses** data visualization and AI to streamline analysis

        **👈 Check out the pages** on the side bar to analyze your own finances!
        """
    )

    # Display technical specifics within an expander
    with st.expander("🧰 Technical Specifics for Developers"):
        st.markdown(
            """
            I built the front end with [Streamlit](https://docs.streamlit.io/library/api-reference)

            Most of the structured data is in [Pandas DataFrames](https://pandas.pydata.org/)

            I used [dotenv](https://www.npmjs.com/package/dotenv) to access my Open AI API Key

            I used [Streamlit-Gsheets](https://github.com/streamlit/gsheets-connection) to connect to Google Sheets data

            I used Open AI's [GPT 3.5 Turbo](https://platform.openai.com/docs/models/gpt-3-5-turbo) model

            I used [Langchain](https://www.langchain.com/), an LLM framework for chat functionality

            [🔗LINK TO GITHUB REPO](https://github.com/hurshkarkhanis/hk-mint)

            """
        )
        
    # Add link back to website
    st.markdown(
        """
        **[⏮ Back to hurshkarkhanis.com](https://www.hurshkarkhanis.com/)**
        """
    )

# Run the Streamlit app
if __name__ == "__main__":
    run()
