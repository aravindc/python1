import os
import re
import json

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

VIDEO_CATEGORIES = '{"1" : "Film & Animation","2" : "Autos & Vehicles","10" : "Music","15" : "Pets & Animals","17" : "Sports","18" : "Short Movies","19" : "Travel & Events","21" : "Videoblogging","20" : "Gaming","22" : "People & Blogs","23" : "Comedy","24" : "Entertainment","25" : "News & Politics","26" : "Howto & Style","27" : "Education","28" : "Science & Technology","29" : "Nonprofits & Activism","30" : "Movies","31" : "Anime/Animation","32" : "Action/Adventure","33" : "Classics","34" : "Comedy","35" : "Documentary","36" : "Drama","37" : "Family","38" : "Foreign","39" : "Horror","40" : "Sci-Fi/Fantasy","41" : "Thriller","42" : "Shorts","43" : "Shows","44" : "Trailers"}'

REGIONS = ['US','CA','DE','FR','IN','CN','FR','RU','AU']

# Authorize the request and store authorization credentials.
def get_authenticated_service():
    return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,developerKey=DEVELOPER_KEY)

# Sample python code for videos.list

def videos_list_most_popular(client, **kwargs):
  # See full sample for function
  #kwargs = remove_empty_kwargs(**kwargs)
  response = client.videos().list(
    **kwargs
  ).execute()

  return print_response(response)

def print_response(response):
  print(response)

# Remove keyword arguments that are not set
def remove_empty_kwargs(**kwargs):
  good_kwargs = {}
  if kwargs is not None:
    for key, value in kwargs.iteritems():
      if value:
        good_kwargs[key] = value
  return good_kwargs



if __name__ == '__main__':
    youtube = get_authenticated_service()
    videoCategoriesObject = json.loads(VIDEO_CATEGORIES)
    for videoCategoryId in videoCategoriesObject:
        for region in REGIONS:
            print(videoCategoryId+":",region)

    #videos_list_most_popular(youtube,
    #    part='snippet,contentDetails,statistics',
    #    chart='mostPopular',
    #    regionCode='GB',
    #    videoCategoryId='24',
    #    pageToken='CAIQAA',
    #    maxResults=1)

    #video_list = youtube.videos().list(part='id,statistics', chart='mostPopular').execute()
    #print(video_list)
    #videos = []
    #for video_result in video_list.get('items',[]):
    #    videos.append('%s,%s,%s,%s,%s' % (video_result['etag'],video_result['statistics']['viewCount'],video_result['statistics']['likeCount'],video_result['statistics']['dislikeCount'],video_result['statistics']['commentCount']))
    #print(videos)
