from googleapiclient.discovery import build
import pandas as pd

API_KEY = "AIzaSyDPQpprcfZoX5Zw9Lh_gR31be7SfFJS0lI"
CHANNEL_ID = "UC8md0UEGj7UbjcZtMjBVrgQ"  

youtube = build('youtube', 'v3', developerKey=API_KEY)


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
                'Title': title,
                'Published': published,
                'Views': int(views),
                'Likes': int(likes),
                'Comments': int(comments)
            })

    return pd.DataFrame(all_data)

video_ids = get_video_ids(CHANNEL_ID)
df = get_video_details(video_ids)
df.to_csv("youtube_data.csv", index=False)
print(df.head())

