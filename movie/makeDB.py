import sqlite3


def update_dir(code, dire):
    try:
        c.execute(
            '''update Mov_info set Mov_director=? where Mov_code=?''',
            (str(dire), str(code)))

        conn.commit()
    except IndexError:
        print('index의 값을 가져올 수 없습니다.')
        pass
    except sqlite3.IntegrityError:
        print('키가 중복되는게 있당.')
        pass

conn = sqlite3.connect('movie.db')

c = conn.cursor()

sql = '''select Mov_code,Mov_director from Mov_info order by Mov_code;'''
# for i in c.execute(sql):
#     print(i[0],i[1])

rs=c.execute(sql)
result=rs.fetchall()
for i in result:
    if i[1]:
        dir = i[1].split(',')
        try:
            if dir[0].__contains__('http'):
                dire = dir[1]
            elif dir[1].__contains__('http'):
                dire=dir[2]
            else:
                dire = dir[0]
            update_dir(dire, i[0])
            print('업데이트완료')
        except IndexError:
            print('index의 값을 가져올 수 없습니다.')
            pass



conn.commit()

conn.close()
