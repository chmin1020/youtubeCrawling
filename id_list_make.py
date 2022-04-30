import csv
from _csv import writer

f = open('videos_id_emotions.csv', 'r', encoding='UTF-8')
rdr = csv.reader(f)

id_list = []

for line in rdr:
    if line[1] not in id_list:
        id_list.append(line[1])

id_list.remove('id')

cnt = 0
for i in id_list:
    cnt = cnt + 1
    with open('selected_id.csv', 'a', newline='', encoding='utf-8') as f_object:
        writer_object = writer(f_object)
        candidate = [i]
        print(i)
        writer_object.writerow(candidate)
        f_object.close()
print("cnt : " + str(cnt))