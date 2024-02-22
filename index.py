from flask import Flask, render_template, redirect, url_for, request
from googleapiclient.discovery import build

app = Flask(__name__)

# Replace 'YOUR_API_KEY' with your actual Google API key
API_KEY = 'Api_keys'

# Define the topics or keywords you are interested in
TOPICS = ['programming', 'electronics', 'personal finance', 'business']

# Number of videos to fetch for each topic
NUM_VIDEOS = 5

def get_youtube_data(api_key, topics, num_videos):
    youtube = build('youtube', 'v3', developerKey=api_key)

    videos = []
    for topic in topics:
        # Get the latest videos for each topic
        request = youtube.search().list(
            part='snippet',
            q=topic,
            order='date',
            type='video',
            maxResults=num_videos
        )
        response = request.execute()

        for item in response['items']:
            video_id = item['id']['videoId']
            video_title = item['snippet']['title']
            thumbnail_url = item['snippet']['thumbnails']['medium']['url']
            videos.append({'id': video_id, 'title': video_title, 'thumbnail': thumbnail_url, 'topic': topic})

    return videos

@app.route('/')
def index():
    search_query = request.args.get('q', '')
    if search_query:
        # If a search query is provided, perform a search based on the query
        # For simplicity, this example uses the same get_youtube_data function
        videos = get_youtube_data(API_KEY, [search_query], NUM_VIDEOS)
    else:
        # Otherwise, fetch videos based on predefined topics
        videos = get_youtube_data(API_KEY, TOPICS, NUM_VIDEOS)

    return render_template('index.html', videos=videos, search_query=search_query)

@app.route('/watch/<video_id>')
def watch(video_id):
    # Redirect to the YouTube video page
    youtube_url = f'https://www.youtube.com/watch?v={video_id}'
    return redirect(youtube_url)

if __name__ == '__main__':
    app.run(debug=True)
