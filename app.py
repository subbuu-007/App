import streamlit as st
import os
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai

# Load environment variables (API key)
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# Configure Google AI with API Key
if api_key:
    genai.configure(api_key=api_key)
else:
    st.error("Google API Key not found. Please set it in the .env file.")

# Custom prompt for AI
prompt = """You are a YouTube video summarizer. You will
be taking the transcript text in Hindi or English and summarizing 
the entire video by providing important points. The transcripted text is appended here: """

# Extract the transcript from a YouTube video URL
def extract_transcript_details(youtube_video_url):
    try:
        # Extract the video ID for both full and short YouTube URLs
        if "youtube.com" in youtube_video_url:
            video_id = youtube_video_url.split("v=")[1].split("&")[0]
        elif "youtu.be" in youtube_video_url:
            video_id = youtube_video_url.split("/")[-1]
        else:
            raise ValueError("Invalid YouTube URL format")

        # Get the transcript using YouTube Transcript API
        transcript_data = YouTubeTranscriptApi.get_transcript(video_id)
        transcript_text = " ".join([i["text"] for i in transcript_data])  # Combine transcript texts
        return transcript_text
    except Exception as e:
        return f"Error: {e}"

# Generate summarized content using Google Gemini AI
def generate_summary(transcript_text, prompt):
    try:
        response = genai.generate_text(prompt + transcript_text)
        return response.result
    except Exception as e:
        return f"Error: {e}"

# Streamlit app layout
def main():
    # Load custom CSS
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    # Display the title and description
    st.markdown(
        """
        <div class="container">
            <header>
                <h1>YouTube Video Summarizer</h1>
                <p>Enter a YouTube video URL to extract its transcript and generate a summary.</p>
            </header>
        </div>
        """, 
        unsafe_allow_html=True
    )

    # Input for YouTube video URL
    youtube_video_url = st.text_input(
        '<label for="youtube-url">YouTube Video URL:</label>',
        value="",
        placeholder="Enter YouTube Video URL",
        label_visibility="visible",
    )

    if youtube_video_url:
        # Extract and display the transcript
        st.markdown('<div id="transcript-section">', unsafe_allow_html=True)
        with st.spinner("Extracting transcript..."):
            transcript_text = extract_transcript_details(youtube_video_url)

        if "Error" in transcript_text:
            st.error(transcript_text)
        else:
            st.markdown(
                f"""
                <h2>Video Transcript:</h2>
                <p>{transcript_text}</p>
                """,
                unsafe_allow_html=True,
            )

            # Generate and display the summarized response
            if st.button("Summarize Video"):
                st.markdown('<div id="summary-section">', unsafe_allow_html=True)
                with st.spinner("Generating summary..."):
                    summary = generate_summary(transcript_text, prompt)
                if "Error" in summary:
                    st.error(summary)
                else:
                    st.markdown(
                        f"""
                        <h2>Summary:</h2>
                        <p>{summary}</p>
                        """,
                        unsafe_allow_html=True,
                    )
                st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    # Footer
    st.markdown(
        """
        <footer>
            <p>Powered by AI & YouTube Transcript API</p>
        </footer>
        """,
        unsafe_allow_html=True,
    )

if __name__ == "__main__":
    main()
