import streamlit as st
import requests
import os

# Configure page
st.set_page_config(page_title="PDF Explainer", page_icon="📚", layout="wide")

# Title and description
st.title("📚 PDF Explainer with AI")
st.markdown("Upload a PDF and get a human-like explanation with audio and video!")

# API configuration
API_URL = "http://localhost:8000"

# File upload
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
custom_prompt = st.text_area(
    "Custom prompt (optional)",
    value="Explain this content in simple terms with practical examples",
    help="Customize how the AI should explain your document"
)

if st.button("Generate Explanation") and uploaded_file is not None:
    with st.spinner("Processing your PDF..."):
        # Prepare request
        files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
        data = {"prompt": custom_prompt}
        
        try:
            # Send request to FastAPI
            response = requests.post(f"{API_URL}/process-pdf/", files=files, data=data)
            
            if response.status_code == 200:
                result = response.json()
                
                # Display explanation
                st.subheader("Explanation")
                st.write(result["explanation"])
                
                # Audio player
                st.subheader("Audio Explanation")
                st.audio(f"{API_URL}/audio/{result['file_id']}")
                
                # Video player
                st.subheader("Video Explanation")
                st.video(f"{API_URL}/video/{result['file_id']}")
                
                # Download buttons
                col1, col2 = st.columns(2)
                with col1:
                    st.download_button(
                        "Download Audio",
                        data=requests.get(f"{API_URL}/audio/{result['file_id']}").content,
                        file_name="explanation.mp3",
                        mime="audio/mpeg"
                    )
                with col2:
                    st.download_button(
                        "Download Video",
                        data=requests.get(f"{API_URL}/video/{result['file_id']}").content,
                        file_name="explanation.mp4",
                        mime="video/mp4"
                    )
            
            else:
                st.error(f"Error: {response.json().get('detail', 'Unknown error')}")
        
        except requests.exceptions.ConnectionError:
            st.error("Could not connect to the API. Make sure the FastAPI server is running.")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

# Instructions
with st.expander("How to use this app"):
    st.markdown("""
    1. Upload a PDF file using the file uploader
    2. Optionally customize the prompt to guide the explanation
    3. Click the 'Generate Explanation' button
    4. Wait for the AI to process your document
    5. View the text explanation, listen to the audio, or watch the video
    6. Download the audio or video for offline use
    """)

# Footer
st.markdown("---")
st.markdown("Built with LangChain, FastAPI, Streamlit, and Google Gemini")