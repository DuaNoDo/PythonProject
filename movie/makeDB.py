import sqlite3
import re
def strclean( stri):
    #         stri = str(stri).strip().replace(' ', '').replace('	', '').replace('''
    # ''','')
    stri = re.sub('\s', '', stri)
    return stri
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
#result=rs.fetchmany(500)
result=rs.fetchall()
for i in result:
    if i[1]:
        dir = i[1].split(',')
        # try:
        #     # if  dir[0].__contains__('http'):
        #     #     dire = dir[1]
        #     # elif dir[1].__contains__('http'):
        #     #     dire=dir[2]
        #     # elif dir[2].__contains__('http'):
        #     #     dire=dir[3]
        #     # else:
        #     #     dire = dir[0]
        #     if not dir[0].__contains__('http'):
        #         dire=dir[0]
        #     else:
        #         continue
        #     update_dir(dire, i[0])
        #     print(dire,'로 업데이트 완ㄹ.')
        # except IndexError:
        #     print('index의 값을 가져올 수 없습니다.')
        #     pass


conn.commit()

conn.close()

