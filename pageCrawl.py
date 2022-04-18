import pandas
import csv
from googleapiclient.discovery import build

api_key = '--secret--'

comments = list()
api_obj = build('youtube', 'v3', developerKey=api_key)

# redial에서 언급된 영화 리스트
movie_list = []
f = open('movies_with_mentions.csv', 'r', encoding='UTF-8')
rdr = csv.reader(f)

# 각 영화 검색 결과 비디오들의 id 리스트
for line in rdr:
    movie_list.append(line[1])

for idx in range(1, 100):  # len(movie_list)):
    find_ids = api_obj.search().list(part='id', q=movie_list[idx], maxResults='8', type='video').execute()
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

df = pandas.DataFrame(comments)
df.to_csv('results.csv', header=['movie_name', 'comment', 'author', 'num_likes'], index=False)
