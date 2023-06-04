import dotenv
import os
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from googleapiclient.discovery import build

dotenv.load_dotenv()
api_key = os.getenv('API_KEY')
def video_comments(video_id):
    count = 0
    # empty list for storing reply
    resposne = {'negative': 0, 'positive': 0}
 
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
                resposne.update({'negative': resposne.get('negative') + 1})
            elif negative != positive:
                resposne.update({'positive': resposne.get('positive') + 1})
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
    return resposne
# Enter video id
video_id = "fJ4JfezknHk"
 
# Call function
print(video_comments(video_id))
