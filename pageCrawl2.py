import csv
from _csv import writer

from selenium import webdriver
import time
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

# redial에서 언급된 영화 리스트
movie_list = []
f = open('movies_with_mentions.csv', 'r', encoding='UTF-8')
rdr = csv.reader(f)

# 각 영화 검색 결과 비디오의 id 리스트
for line in rdr:
    movie_list.append(line[1])
f.close()

'''
#비디오 id
video_list = []
f = open('videos.CSV', 'r', encoding='UTF-8')
rdr = csv.reader(f)

# 각 영화 검색 결과 비디오들의 id 리스트
for line in rdr:
    video_list.append(line[1])
f.close()
'''

# selenium
options = webdriver.ChromeOptions()
options.add_argument("headless")
options.add_argument('--mute-audio')

driver = webdriver.Chrome(options=options)
driver.set_window_size(800, 600)
driver.get("https://www.youtube.com/watch?v=W2MgsPqheRc")
driver.implicitly_wait(3)

time.sleep(1.5)

driver.execute_script("window.scrollTo(0, 800)")
time.sleep(3)

# 페이지 끝까지 스크롤
last_height = driver.execute_script("return document.documentElement.scrollHeight")

while True:
    driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
    time.sleep(1.5)

    new_height = driver.execute_script("return document.documentElement.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

time.sleep(1.5)

# 팝업 닫기
try:
    driver.find_element(by=By.CSS_SELECTOR, value="#dismiss-button > a").click()
except:
    pass

# 대댓글 모두 열기
buttons = driver.find_elements(by=By.CSS_SELECTOR, value="#more-replies > a")

time.sleep(1.5)

for button in buttons:
    button.send_keys(Keys.ENTER)
    time.sleep(1.5)
    button.click()

time.sleep(1.5)

# 정보 추출하기
html_source = driver.page_source
soup = BeautifulSoup(html_source, 'html.parser')

id_list = soup.select("div#header-author > h3 > #author-text > span")
comment_list = soup.select("yt-formatted-string#content-text")

with open('comments.csv', 'a', newline='', encoding='utf-8') as f_object:
    for i in range(len(comment_list)):
        temp_id = id_list[i].text
        temp_id = temp_id.replace('\n', '')
        temp_id = temp_id.replace('\t', '')
        temp_id = temp_id.replace('    ', '')

        temp_comment = comment_list[i].text
        temp_comment = temp_comment.replace('\n', '')
        temp_comment = temp_comment.replace('\t', '')
        temp_comment = temp_comment.replace('    ', '')

        writer_object = writer(f_object)
        writer_object.writerow([movie_list[2], temp_id, temp_comment])
    f_object.close()

driver.quit()

#pd_data = {"movie_name": movie_name, "id": id_final, "comments": comment_final}
#youtube_pd = pd.DataFrame(pd_data)
#youtube_pd.to_csv('comments.csv', header=['movie_name', 'id', 'comments'], index=False)



# youtube_pd = pd.DataFrame(pd_data)
# youtube_pd.to_excel('youtube.xlsx')
