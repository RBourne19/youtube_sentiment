import dotenv
import os
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from googleapiclient.discovery import build

dotenv.load_dotenv()
api_key = os.getenv('API_KEY')
def video_comments(video_id):
    count = 0
    negative = 0 
    positive = 0
    neutral = 0
    # empty list for storing reply
    
 
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
            negativeScore = SentimentIntensityAnalyzer().polarity_scores(comment)['neg']
            positiveScore = SentimentIntensityAnalyzer().polarity_scores(comment)['pos']
            if(negativeScore > positiveScore):
                negative += 1
            elif negativeScore != positiveScore:
                positive += 1
            else:
                neutral += 1
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

    
    return {'negative': negative, 'positive': positive, 'neutral': neutral, 'total': count}
# Enter video id
video_id = "wdSXpQcjj0I"
 
# Call function
print(video_comments(video_id))
