import os
import re

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow

# URL to get top channel in each videoCategories
#https://www.googleapis.com/youtube/v3/videoCategories?part=snippet&regionCode=UK&key=AIzaSyAHp_6KLQIzlfrpm0h6LS5TzGZLQHdDZyM
#https://www.googleapis.com/youtube/v3/videos?part=contentDetails&chart=mostPopular&regionCode=IN&maxResults=200&key=AIzaSyAHp_6KLQIzlfrpm0h6LS5TzGZLQHdDZyM
#URL to get top videos fora particular videoCategoryId with Views, Likes, Dislikes and Comments count
#https://www.googleapis.com/youtube/v3/videos?part=statistics&chart=mostPopular&videoCategoryId=24&regionCode=IN&maxResults=50&key=AIzaSyAHp_6KLQIzlfrpm0h6LS5TzGZLQHdDZyM

DEVELOPER_KEY = 'AIzaSyAHp_6KLQIzlfrpm0h6LS5TzGZLQHdDZyM'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

# Authorize the request and store authorization credentials.
def get_authenticated_service():
    return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,developerKey=DEVELOPER_KEY)

if __name__ == '__main__':
    youtube = get_authenticated_service()
    print(youtube)
