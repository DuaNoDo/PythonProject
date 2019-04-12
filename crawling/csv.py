import _csv
import sqlite3

con = sqlite3.connect('db.sqlite')

con.text_factory = str

cur = con.cursor()

csv_file = open("item.csv", encoding="utf-8")

csv_reader = _csv.reader(csv_file)

item_list = list(csv_reader)

item_list = item_list[1:]

for item in item_list:
    item[1] = item[1].strip()
    item[2] = item[2].strip()

print(item_list)

cur.executemany("insert into item_info values(?,?,?)", item_list)

con.commit()
