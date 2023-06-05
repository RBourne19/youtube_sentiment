import dotenv
import os
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from googleapiclient.discovery import build

dotenv.load_dotenv()
api_key = os.getenv('API_KEY')
def video_comments(video_id):
    count = 0
    # empty list for storing reply
    response = {'negative': 0, 'positive': 0, 'neutral': 0, 'total': 0}
 
    # creating youtube resource object
    youtube = build('youtube', 'v3',
                    developerKey=api_key)
 
    # retrieve youtube video results
    video_response=youtube.commentThreads().list(
    part='snippet,replies',
    videoId=video_id,
    textFormat='plainText'
    ).execute()
    
    # iterate video response
    while video_response:
        # extracting required info
        # from each result object
        for item in video_response['items']:
            # Extracting comments
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            print(comment)
            negative = SentimentIntensityAnalyzer().polarity_scores(comment)['neg']
            positive = SentimentIntensityAnalyzer().polarity_scores(comment)['pos']
            if(negative > positive):
                response.update({'negative': response.get('negative') + 1})
            elif negative != positive:
                response.update({'positive': response.get('positive') + 1})
            else:
                response.update({'neutral': response.get('neutral') + 1})
            # counting number of reply of comment
            replycount = item['snippet']['totalReplyCount']
            count += 1    
        # Again repeat
        if 'nextPageToken' in video_response:
            video_response = youtube.commentThreads().list(
                    part = 'snippet,replies',
                    videoId = video_id,
                    pageToken = video_response['nextPageToken'],
                    textFormat = 'plainText'
                ).execute()
        else:
            break

    response.update({'total' : count})
    return response
# Enter video id
video_id = "B-tL7220WYc"
 
# Call function
print(video_comments(video_id))
