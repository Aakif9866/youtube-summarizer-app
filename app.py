import streamlit as st 
from dotenv import load_dotenv
import google.generativeai as genai 
import os 

from youtube_transcript_api import YouTubeTranscriptApi, _errors

def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("v=")[-1].split("&")[0]
        
        # Add proxy
        proxies = {
            "http": "http://your_proxy_ip:port",
            "https": "http://your_proxy_ip:port"
        }

        transcript_text = YouTubeTranscriptApi.get_transcript(video_id, proxies=proxies)

        transcript = " ".join([i["text"] for i in transcript_text])
        return transcript

    except _errors.RequestBlocked:
        return "❌ YouTube blocked the request. Use a proxy or run locally."
    except _errors.TranscriptsDisabled:
        return "❌ Transcripts are disabled for this video."
    except Exception as e:
        return f"❌ Error: {e}"


load_dotenv()  # this will load all the variables

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

prompt = """You are YouTube video summarizer. You will be taking the transcript text
and summarizing the entire video and providing the important summary in points
within 250 words. Please provide the summary of the text given here:  """


# Getting the summary from Gemini Pro
def generate_gemini_content(transcript_text, prompt):
    model = genai.GenerativeModel("gemini-2.5-pro")
    response = model.generate_content(prompt + transcript_text)
    return response.text

st.title("YouTube Transcript to Detailed Notes Converter")
youtube_link = st.text_input("Enter YouTube Video Link:")

if youtube_link:
    video_id = youtube_link.split("=")[1]
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_container_width=True)

if st.button("Get Detailed Notes"):
    transcript_text = extract_transcript_details(youtube_link)

    if transcript_text:
        summary = generate_gemini_content(transcript_text, prompt)
        st.markdown("## Detailed Notes:")
        st.write(summary)
