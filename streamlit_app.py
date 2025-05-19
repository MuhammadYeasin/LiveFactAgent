import streamlit as st
import requests
import time

def main():
    st.title("LiveFactAgent: Real-Time Speech Fact-Checker")
    st.write("Speak into your microphone to fact-check claims in real time.")
    
    # Create a placeholder for displaying results
    results_container = st.empty()
    
    # Create a simple text input for manual fact-checking (as a fallback)
    st.subheader("Manual Fact-Checking")
    claim_text = st.text_input("Enter a claim to fact-check:")
    
    if st.button("Check Claim"):
        if claim_text:
            try:
                # Make a POST request to the fact-check endpoint
                response = requests.post(
                    "http://localhost:8000/fact-check", 
                    json={"claim": claim_text}
                )
                
                if response.status_code == 200:
                    result = response.json()
                    st.success("Fact check complete!")
                    st.write(f"**Claim:** {result.get('claim')}")
                    st.write(f"**Status:** {result.get('status')}")
                    
                    # Display citations
                    if result.get('citations'):
                        st.subheader("Citations:")
                        for citation in result.get('citations'):
                            st.write(f"- {citation.get('text')} ([source]({citation.get('url')}))")
                else:
                    st.error(f"Error: {response.status_code}")
                    st.write(response.text)
            except Exception as e:
                st.error(f"Error connecting to server: {str(e)}")
    
    # Instructions for WebSocket connection
    st.subheader("Microphone Connection Status")
    status = st.empty()
    status.warning("WebSocket functionality requires additional configuration. Using manual input for now.")
    
    st.markdown("""
    ### Using the Application
    
    1. Make sure the FastAPI server is running in a separate terminal with `python server.py`
    2. Enter factual claims in the text box above
    3. Click "Check Claim" to verify the claim
    
    ### Example Claims to Test
    
    - The Earth is flat
    - Paris is the capital of France
    - The Eiffel Tower is 1000 meters tall
    """)

if __name__ == "__main__":
    main()