import streamlit as st  
from logi.crew import Logi  
  
st.set_page_config(page_title="Logistics CrewAI Agent", page_icon="🚚")  
  
st.title("🚚 Logistics Agent")  
st.write("The agent writes RFQs and evaluates carriers for shipping materials.")
st.write("Enter details to run the agent:")  
  
with st.form("crew_form"):  
    material = st.text_input("Material", value="Insulin")  
    location = st.text_input("Location", value="UK")  
    run_btn = st.form_submit_button("Run Agent")  
  
if run_btn: 
    if not material or not location:
        st.warning("Please enter both Material and Location.")
    else:
        st.info("Running Crew... Please wait.")  
        # Assemble the dictionary of inputs as in your main.py  
        inputs = {  
            "material": material,  
            "location": location,  
            "script": "knowledge/evaluate_carrier.py",  # Hardcoded
        }  
        try:  
            def run_stream():
                yield from Logi().crew().kickoff(inputs=inputs)
            st.write_stream(run_stream)
        except Exception as e:  
            st.error(f"An error occurred while running the crew: {e}")
  
st.write("---")  
st.caption("Powered by CrewAI & Streamlit.")  