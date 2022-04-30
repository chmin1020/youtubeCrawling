from _csv import writer
from googleapiclient.discovery import build
import csv

api_key = 'AIzaSyCvygDGjp2T9CQkGVtOLUv7w4TaVe0sM8Y'
comments = list()
api_obj = build('youtube', 'v3', developerKey=api_key)

#selected id 파일 열기
idf = open('selected_id.csv', 'r', encoding='UTF-8')
rdr = csv.reader(idf)
id_list = []
for line in rdr:
    id_list.append(line)

idf = open('selected_id.csv', 'a', encoding='UTF-8')


# redial에서 언급된 영화 리스트
tag_list = []
f = open('genome-tags.csv', 'r', encoding='UTF-8')
rdr = csv.reader(f)

# 각 영화 검색 결과 비디오들의 id 리스트
for line in rdr:
    tag_list.append(line[1])

#태그 102까지
for keyword in tag_list:
    query = str(keyword) + " movies recommend"
    find_ids = api_obj.search().list(part='id', q=query, order='relevance', maxResults='10').execute()
    print(find_ids)
    cnt = 0
    for its in find_ids['items']:
        if 'videoId' not in its['id']:
            continue
        if its['id']['videoId'] in tag_list:
            continue
        else:
            tplist = [its['id']['videoId']]
            tag_list.append(its['id']['videoId'])
            writer_object = writer(idf)
            writer_object.writerow(tplist)

        cnt = cnt + 1

        videos = [query, its['id']['videoId']]
        with open('videos_id_emotions.csv', 'a', newline='', encoding='utf-8') as f_object:
            writer_object = writer(f_object)
            writer_object.writerow(videos)
            f_object.close()

        if cnt == 4:
            break