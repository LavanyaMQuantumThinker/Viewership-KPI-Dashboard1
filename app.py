from googleapiclient.discovery import build
import pandas as pd
import streamlit as st
import numpy as np
import plotly.express as px

# YouTube API credentials
API_KEY = "AIzaSyDPQpprcfZoX5Zw9Lh_gR31be7SfFJS0lI"
CHANNEL_ID = "UC8md0UEGj7UbjcZtMjBVrgQ"

youtube = build('youtube', 'v3', developerKey=API_KEY)

# Get video IDs from the channel
def get_video_ids(channel_id):
    request = youtube.search().list(
        part="id",
        channelId=channel_id,
        maxResults=50,
        order="date",
        type="video"
    )
    response = request.execute()
    video_ids = [item['id']['videoId'] for item in response['items']]
    return video_ids

# Get video details
def get_video_details(video_ids):
    all_data = []
    for i in range(0, len(video_ids), 50):
        request = youtube.videos().list(
            part="snippet,statistics",
            id=','.join(video_ids[i:i+50])
        )
        response = request.execute()
        for video in response['items']:
            title = video['snippet']['title']
            published = video['snippet']['publishedAt']
            views = video['statistics'].get('viewCount', 0)
            likes = video['statistics'].get('likeCount', 0)
            comments = video['statistics'].get('commentCount', 0)
            all_data.append({
                'title': title,
                'published': published,
                'views': int(views),
                'likes': int(likes),
                'comments': int(comments)
            })
    return pd.DataFrame(all_data)

# Fetch data
video_ids = get_video_ids(CHANNEL_ID)
df = get_video_details(video_ids)

# Clean data
df['published'] = pd.to_datetime(df['published'])
df['engagement_rate'] = (df['likes'] + df['comments']) / df['views']
df = df.sort_values(by='published')
df['post_frequency'] = df['published'].diff().dt.days

# Streamlit dashboard
st.title("📊 Viewership KPI Dashboard")
st.write("Analyze multi-platform video performance for Behindwoods")

# KPI section
st.subheader("Key Performance Indicators")
st.metric("Total Views", f"{df['views'].sum():,}")
st.metric("Total Likes", f"{df['likes'].sum():,}")
st.metric("Average Engagement Rate", f"{df['engagement_rate'].mean():.2%}")

# Line Chart: Views over time
st.subheader("📈 Views Over Time")
daily_views = df.groupby("published")["views"].sum().reset_index()
fig_line = px.line(daily_views, x="published", y="views", title="Total Daily Views")
st.plotly_chart(fig_line)

# Bar Chart: Top 5 videos
st.subheader("🏆 Top 5 Performing Videos")
top_videos = df.sort_values(by="views", ascending=False).head(5)
fig_bar = px.bar(top_videos, x="title", y="views", color="views", title="Top 5 Videos by Views")
st.plotly_chart(fig_bar)

# Pie Chart: Likes vs Comments
st.subheader("❤️ Likes vs 💬 Comments Distribution")
engagement = pd.DataFrame({
    'Type': ['Likes', 'Comments'],
    'Count': [df['likes'].sum(), df['comments'].sum()]
})
fig_pie = px.pie(engagement, names='Type', values='Count', title="Likes vs Comments")
st.plotly_chart(fig_pie)
