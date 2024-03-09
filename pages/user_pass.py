import streamlit as st
import os

correct_username = os.getenv('USERNAME')
correct_password = os.getenv('PASSWORD')
my_key = os.getenv('OPEN_AI_API_KEY')
st.write(correct_username)
st.write(correct_password)







