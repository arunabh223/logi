import streamlit as st

st.title("Logistics Agent")
st.write("A prototype logistics agent created for the Biocon SCM team.")
prompt = st.chat_input("Give me a task....")
print(prompt)