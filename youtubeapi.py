import os
import re
import json
import datetime
import codecs

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow

# URL to get top channel in each videoCategories
# https://www.googleapis.com/youtube/v3/videoCategories?part=snippet&regionCode=UK&key=AIzaSyAHp_6KLQIzlfrpm0h6LS5TzGZLQHdDZyM
# https://www.googleapis.com/youtube/v3/videos?part=contentDetails&chart=mostPopular&regionCode=IN&maxResults=200&key=AIzaSyAHp_6KLQIzlfrpm0h6LS5TzGZLQHdDZyM
# URL to get top videos fora particular videoCategoryId with Views, Likes, Dislikes and Comments count
# https://www.googleapis.com/youtube/v3/videos?part=statistics&chart=mostPopular&videoCategoryId=24&regionCode=IN&maxResults=50&key=AIzaSyAHp_6KLQIzlfrpm0h6LS5TzGZLQHdDZyM

DEVELOPER_KEY = 'AIzaSyAHp_6KLQIzlfrpm0h6LS5TzGZLQHdDZyM'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

# "18" : "Short Movies","21" : "Videoblogging","30" : "Movies","31" : "Anime/Animation","32" : "Action/Adventure",
# "33" : "Classics","34" : "Comedy","35" : "Documentary","36" : "Drama","37" : "Family","38" : "Foreign",
# "39" : "Horror","40" : "Sci-Fi/Fantasy","41" : "Thriller","42" : "Shorts","43" : "Shows","44" : "Trailers"

# VIDEO_CATEGORIES = '{"1" : "Film & Animation","2" : "Autos & Vehicles","10" : "Music","15" : "Pets & Animals",' \
#                   '"17" : "Sports","19" : "Travel & Events","20" : "Gaming","22" : "People & Blogs","23" : "Comedy",' \
#                   '"24" : "Entertainment","25" : "News & Politics","26" : "Howto & Style","27" : "Education",' \
#                   '"28" : "Science & Technology","29" : "Nonprofits & Activism"}'
VIDEO_CATEGORIES = '{"1": "Film & Animation"}'

# REGIONS = ['US', 'CA', 'DE', 'FR', 'IN', 'CN', 'FR', 'RU', 'AU', 'GB', 'JP']
REGIONS = ['US']

now = datetime.datetime.now()


# Authorize the request and store authorization credentials.
def get_authenticated_service():
    return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)


# Sample python code for videos.list

def videos_list_most_popular(vcatId, region, client, **kwargs):
    # See full sample for function
    response = None
    while response is None:
        try:
            response = client.videos().list(**kwargs).execute()
        except HttpError as e:
            print('%s not available in %s' % (vcatId, region))
            break
    return write_data(response, vcatId, region)


def parse_data(response):
    return response


def write_data(response, vcatId, region):
    if response is not None:
        for video in response.get('items', []):
            # print(video)
            f = codecs.open(now.strftime("%Y%m%d") + '.csv', 'a', 'utf-8')
            # f.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n' %
            mid = video['id'] if 'id' in video else None
            if 'snippet' in video:
                mtitle = video['snippet']['title'].replace(',', ' ') if 'title' in video['snippet'] else None
                mpublishedAt = video['snippet']['publishedAt'] if 'publishedAt' in video['snippet'] else None
                mlanguage = video['snippet']['defaultAudioLanguage'] if 'defaultAudioLanguage' in video['snippet'] else None
                if mlanguage is None:
                    mlanguage = video['snippet']['defaultLanguage'] if 'defaultLanguage' in video['snippet']  else None
            else:
                mtitle = None
                mpublishedAt = None
                mlanguage = None
            if 'statistics' in video:
                # print(video['statistics'])
                mviewCount = video['statistics']['viewCount'] if 'viewCount' in video['statistics'] else 0
                mlikeCount = video['statistics']['likeCount'] if 'likeCount' in video['statistics'] else 0
                mdislikeCount = video['statistics']['dislikeCount'] if 'dislikeCount' in video['statistics'] else 0
                mcommentCount = video['statistics']['commentCount'] if 'commentCount' in video['statistics'] else 0
            else:
                print(video)
                mviewCount = 0
                mlikeCount = 0
                mdislikeCount = 0
                mcommentCount = 0

            f.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n' %
                    (
                        now.strftime("%Y-%m-%d"),
                        vcatId, region,
                        mid,
                        mtitle,
                        # video['snippet']['description'].replace('\n',' ').replace(',',' ')  if 'description' in video['snippet'] else None,
                        mpublishedAt,
                        mviewCount,
                        mlikeCount,
                        mdislikeCount,
                        mcommentCount,
                        mlanguage
                    ))  # Give your csv text here.
            ## Python will convert \n to os.linesep
            f.close()


if __name__ == '__main__':
    try:
        os.remove(now.strftime("%Y%m%d") + '.csv')
    except OSError:
        pass
    youtube = get_authenticated_service()
    videoCategoriesObject = json.loads(VIDEO_CATEGORIES)
    for vcatId in videoCategoriesObject:
        for region in REGIONS:
            videos_list_most_popular(vcatId, region, youtube,
                                     part='statistics,snippet',
                                     chart='mostPopular',
                                     regionCode=region,
                                     videoCategoryId=vcatId,
                                     maxResults=50)

    # videos_list_most_popular(youtube,
    #    part='snippet,contentDetails,statistics',
    #    chart='mostPopular',
    #    regionCode='GB',
    #    videoCategoryId='24',
    #    pageToken='CAIQAA',
    #    maxResults=1)

    # video_list = youtube.videos().list(part='id,statistics', chart='mostPopular').execute()
    # print(video_list)
    # videos = []
    # for video_result in video_list.get('items',[]):
    #    videos.append('%s,%s,%s,%s,%s' % (video_result['etag'],video_result['statistics']['viewCount'],
    # video_result['statistics']['likeCount'],video_result['statistics']['dislikeCount'],
    # video_result['statistics']['commentCount']))
    # print(videos)
