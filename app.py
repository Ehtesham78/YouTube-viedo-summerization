import streamlit as st 
from dotenv import load_dotenv
import os
load_dotenv() # load environment variables from .env file
import google.generativeai as genai

from youtube_transcript_api import YouTubeTranscriptApi 

genai.configure(api_key= os.getenv("GOOGLE_API_KEY")) # configure the generative AI API 

prompt ="""you are youtube video sumarizer . you will be taking the transcript of a youtube video and generating a summary of the video and providing the important 
summary in points within 500 words. please provide the youtube video url and click on the generate summary button to get the summary of the video. """


## getting the transcript data from the youtube video url
def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("=")[1]
        print(video_id)
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id) 
        
        transcript = ""
        for i in transcript_text:
            transcript +=  " " + i['text']
            
        return transcript
    
    except Exception as e:
        raise e
## getting the summary based on prompt form google gemini pro 
def generate_gemini_content(transcript_text, prompt ):
    
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt+transcript_text)
    return response.text 


st.title("Youtube Video Summarizer")
youtube_link = st.text_input("Enter the youtube video url")

if youtube_link:
    video_id = youtube_link.split("=")[1]
    print(video_id)
    st.image(f"https://img.youtube.com/vi/{video_id}/0.jpg",use_column_width=True)
    
if st.button("Generate Summary"):
    transcript_text = extract_transcript_details(youtube_link)
    
    if transcript_text:
        summary = generate_gemini_content(transcript_text, prompt)
        st.markdown("## Summary of the video")
        st.write(summary)
    
    