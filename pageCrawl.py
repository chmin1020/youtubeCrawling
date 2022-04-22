from _csv import writer
import pandas
import csv
from googleapiclient.discovery import build

api_key = 'AIzaSyCvygDGjp2T9CQkGVtOLUv7w4TaVe0sM8Y'
comments = list()
api_obj = build('youtube', 'v3', developerKey=api_key)

'''
# redial에서 언급된 영화 리스트
movie_list = []
f = open('movies_with_mentions.csv', 'r', encoding='UTF-8')
rdr = csv.reader(f)


# 각 영화 검색 결과 비디오들의 id 리스트
for line in rdr:
    movie_list.append(line[1])
'''
query = "movies for kids recommend"
find_ids = api_obj.search().list(part='id', q= query, maxResults='4', type='video').execute()
for its in find_ids['items']:
    videos = [query, its['id']['videoId']]
    with open('videos_id_emotions.csv', 'a', newline='', encoding='utf-8') as f_object:
        writer_object = writer(f_object)
        writer_object.writerow(videos)
        f_object.close()
    '''
    comments = []
    for its in find_ids['items']:
        video_id = its['id']['videoId']
        try:
            response = api_obj.commentThreads().list(part='snippet,replies', videoId=video_id, order='relevance',
                                                     maxResults=100)
            while response:
                for item in response['items']:
                    comment = item['snippet']['topLevelComment']['snippet']
                    comments.append(
                        [movie_list[idx], comment['textDisplay'], comment['authorDisplayName'], comment['likeCount']])

                    # 답글 있을 경우 (따로 처리해야 할 듯)
                    if item['snippet']['totalReplyCount'] > 0 and 'replies' in item:
                        reply = item['replies']['comments']
                        for each_reply in reply:
                            comments.append([movie_list[idx], each_reply['snippet']['textDisplay'],
                                             each_reply['snippet']['authorDisplayName'],
                                             each_reply['snippet']['likeCount']])

                if 'nextPageToken' in response:
                    response = api_obj.commentThreads().list(part='snippet,replies', videoId=video_id,
                                                             order='relevance',
                                                             pageToken=response['nextPageToken'],
                                                             maxResults=100).execute()
                else:
                    break
        except:
            continue
    '''

#df = pandas.DataFrame(comments)
#df.to_csv('videos.csv', header=['movie_name', 'title', 'videoID'], index=False)
