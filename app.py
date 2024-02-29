import streamlit as st
from dotenv import load_dotenv
from googleapiclient.discovery import build
import os

load_dotenv()

# Set up your Google API key in the environment variables
# You need to enable the YouTube Data API v3 in your Google Cloud Console
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)


def get_channel_videos(channel_id, max_results=10):
    videos = []
    request = youtube.search().list(
        part="snippet",
        channelId=channel_id,
        order="date",
        type="video",
        maxResults=max_results
    )
    response = request.execute()
    for item in response["items"]:
        videos.append(item)
    return videos


def get_video_comments(video_id):
    comments = []
    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        textFormat="plainText"
    )
    while request:
        response = request.execute()
        for item in response["items"]:
            comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
            comments.append(comment)
        request = youtube.commentThreads().list_next(request, response)
    return comments


st.title("Youtube Video Comments Extractor")
channel_id = st.text_input("Enter Youtube Channel ID:")

if st.button("Get Comments of Top 10 Most Recent Videos"):
    if channel_id:
        videos = get_channel_videos(channel_id)
        if videos:
            for video in videos:
                video_id = video['id']['videoId']
                st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)
                comments = get_video_comments(video_id)
                st.markdown(f"## Comments for Video: {video['snippet']['title']}")
                if comments:
                    for comment in comments:
                        st.write(comment)
                else:
                    st.write("No comments found for this video.")
                st.markdown("---")
        else:
            st.write("No videos found for this channel.")
    else:
        st.write("Please enter a valid YouTube channel ID.")
