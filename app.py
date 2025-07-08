import streamlit as st
import os
from src.utils.output_handler import capture_output
from logi.crew import Logi

#--------------------------------#
#         Streamlit App          #
#--------------------------------#
# Configure the page
st.set_page_config(
    page_title="CrewAI Logistics Agent",
    page_icon="🕵️‍♂️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Main layout
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.title("🔍 :red[CrewAI] Logistics Agent", anchor=False)
    st.divider()
    st.write("""
                The agent
                \n 1. Writes RFQs for shipping materials.
                \n 2. Evaluates carriers for shipping materials based on their historical performance.
             """)

# Create two boxes for the input section
with col2:
    with st.form("crew_form"):
        st.write("Enter the material and location")  
        material = st.text_input("Material", value="Insulin")  
        location = st.text_input("Location", value="UK")  
        run_btn = st.form_submit_button("Run Agent", type="primary")

if run_btn:
    with st.status("🤖 Agent running...", expanded=True) as status:
        try:
            # Create persistent container for process output with fixed height.
            process_container = st.container(height=300, border=True)
            output_container = process_container.container()
            
            # Single output capture context.
            inputs = {  
            "material": material,  
            "location": location,
            }  
            with capture_output(output_container):
                result = Logi().crew().kickoff(inputs=inputs)
                status.update(label="✅ Tasks completed!", state="complete", expanded=False)
        except Exception as e:
            status.update(label="❌ Error occurred", state="error")
            st.error(f"An error occurred: {str(e)}")
            st.stop()
    
    # Convert CrewOutput to string for display and download
    result_text = str(result)
    
    # Display the final result
    st.markdown(result_text)
    
    # Create download buttons
    st.divider()
    download_col1, download_col2, download_col3 = st.columns([1, 2, 1])
    with download_col2:
        st.markdown("### 📥 Download Report")
        
        # Download as Markdown
        st.download_button(
            label="Download Report",
            data=result_text,
            file_name="research_report.md",
            mime="text/markdown",
            help="Download the research report in Markdown format"
        )

# Add footer
st.divider()
footer_col1, footer_col2, footer_col3 = st.columns([1, 2, 1])
with footer_col2:
    st.caption("Made with ❤️ using [CrewAI](https://crewai.com) and [Streamlit](https://streamlit.io)")