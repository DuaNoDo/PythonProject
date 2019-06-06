import os
import sqlite3
from flask import Flask, render_template, request, current_app
from flask_pager import Pager

app = Flask(__name__)

app.debug = True

app.config['PAGE_SIZE'] = 287
app.config['VISIBLE_PAGE_COUNT'] = 10


def get_db_con() -> sqlite3.connect:
    return sqlite3.connect("movie.db")


@app.route("/")
def index():
    with get_db_con() as con:
        cur = con.cursor()

        mov_info_all = "select * from Mov_info"

        mov_info_all = cur.execute(mov_info_all)
        mov_info_all = list(mov_info_all.fetchall())

        action = "select * from mov_info where mov_info like '%'|| '액션' ||'%' order by mov_date desc"

        mov_info_action = cur.execute(action.format('action'))
        mov_info_action = list(mov_info_action.fetchall())

        romance = "select * from mov_info where mov_info like '%'|| '로맨스' ||'%' order by mov_date desc"

        mov_info_romance = cur.execute(romance.format('romance'))
        mov_info_romance = list(mov_info_romance.fetchall())

        horror = "select * from mov_info where mov_info like '%'|| '공포' ||'%' order by mov_date desc"

        mov_info_horror = cur.execute(horror.format('horror'))
        mov_info_horror = list(mov_info_horror.fetchall())

        ani = "select * from mov_info where mov_info like '%'|| '애니메이션' ||'%' order by mov_date desc"

        mov_info_ani = cur.execute(ani.format('ani'))
        mov_info_ani = list(mov_info_ani.fetchall())

        url = 'http://www.kobis.or.kr/'

        return render_template('index.html', mov_info_all=mov_info_all, url=url, mov_info_action=mov_info_action,
                               mov_info_romance=mov_info_romance, mov_info_horror=mov_info_horror,
                               mov_info_ani=mov_info_ani)


@app.route('/catalog' , methods=['POST','GET'])
@app.route('/catalog')
@app.route('/catalog/')
def catalog():
    with get_db_con() as con:
        cur = con.cursor()

        mov_info_all = "select * from Mov_info"

        mov_info_all = cur.execute(mov_info_all)
        mov_info_all = list(mov_info_all.fetchall())

        action = "select * from mov_info where mov_info like '%액션%' order by mov_date desc"

        mov_info_action = cur.execute(action.format('action'))
        mov_info_action = list(mov_info_action.fetchall())

        romance = "select * from mov_info where mov_info like '%로맨스%' order by mov_date desc"

        mov_info_romance = cur.execute(romance.format('romance'))
        mov_info_romance = list(mov_info_romance.fetchall())

        horror = "select * from mov_info where mov_info like '%공포%' order by mov_date desc"

        mov_info_horror = cur.execute(horror.format('horror'))
        mov_info_horror = list(mov_info_horror.fetchall())

        ani = "select * from mov_info where mov_info like '%애니메이션%' order by mov_date desc"

        mov_info_ani = cur.execute(ani.format('ani'))
        mov_info_ani = list(mov_info_ani.fetchall())

        url = 'http://www.kobis.or.kr/'

        total_all = 'select count(*) from mov_info'
        total_all = cur.execute(total_all)
        total_all = int(total_all.fetchone()[0])

        page = int(request.args.get('page', 1))
        pager = Pager(page, total_all)
        pages = pager.get_pages()
        skip = (page - 1) * 24
        data_to_show = mov_info_all[skip: skip + 24]
        len_to_show=len(data_to_show)
        # print(data_to_show)
        return render_template('catalog.html', url=url, mov_info_action=mov_info_action,
                               mov_info_romance=mov_info_romance, mov_info_horror=mov_info_horror,
                               mov_info_ani=mov_info_ani, pages=pages, data_to_show=data_to_show,len_to_show=len_to_show)

@app.route('/wsearch',methods=['GET','POST'])
def catalogWS():
        if request.method=='GET':
            keyword = request.values["keyword"]
            len_to_show=24
            with get_db_con() as con:
                cur = con.cursor()

                mov_info_all = '''select * from Mov_info  where mov_name_kor like '%'''+keyword+'''%' or mov_name_eng like '%'''+keyword+'''%' or mov_director like '%'''+keyword+'''%' or mov_actor like '%'''+keyword+'''%' order by mov_date desc'''

                mov_info_all = cur.execute(mov_info_all)
                mov_info_all = list(mov_info_all.fetchall())

                url = 'http://www.kobis.or.kr/'

                total_all = '''select count(*) from mov_info where mov_name_kor like '%'''+keyword+'''%' or mov_name_eng like '%'''+keyword+'''%' or mov_director like '%'''+keyword+'''%' or mov_actor like '%'''+keyword+'''%' order by mov_date desc'''
                total_all = cur.execute(total_all)
                total_all = int(total_all.fetchone()[0])

                if total_all>=24 :
                    page = int(request.args.get('page', 1))
                    pager = Pager(page, total_all)
                    pages = pager.get_pages()
                    skip = (page - 1) * 24
                    data_to_show = mov_info_all[skip: skip + 24]
                    len_to_show= len(data_to_show)
                else:
                    pages=[1]
                    data_to_show = mov_info_all
                    len_to_show = len(data_to_show)
                # print(len(data_to_show))
                # print(data_to_show)
                return render_template('catalog.html', url=url, pages=pages, data_to_show=data_to_show,len_to_show=len_to_show)


@app.route('/catalog/search',methods=['GET','POST'])
def catalogS():
        if request.method=='GET':
            cate = request.values["cate"]
            time=request.values['time']
            with get_db_con() as con:
                cur = con.cursor()

                mov_info_all = '''select * from Mov_info  where mov_info like '%'''+cate+'''%' and mov_info like '%'''+time+'''%' order by mov_date desc'''

                mov_info_all = cur.execute(mov_info_all)
                mov_info_all = list(mov_info_all.fetchall())

                url = 'http://www.kobis.or.kr/'

                total_all = '''select count(*) from mov_info where mov_info like '%'''+cate+'''%' and mov_info like '%'''+time+'''%' order by mov_date desc'''
                total_all = cur.execute(total_all)
                total_all = int(total_all.fetchone()[0])
                print(total_all)
                page = int(request.args.get('page', 1))
                pager = Pager(page, total_all)
                pages = pager.get_pages()
                skip = (page - 1) * 24
                data_to_show = mov_info_all[skip: skip + 24]
                len_to_show=len(data_to_show)
                # print(data_to_show)
                return render_template('catalog.html', url=url, pages=pages, data_to_show=data_to_show,len_to_show=len_to_show)



@app.route('/details')
@app.route('/details/<int:mov_code>/')
@app.route('/details/<int:mov_code>')
def details(mov_code):
    with get_db_con() as con:
        cur = con.cursor()

        mov_info_details = "select * from Mov_info where mov_code = {}"

        mov_info_details = cur.execute(mov_info_details.format(mov_code))
        mov_info_details = list(mov_info_details.fetchall())

        # CINEMA
        mov_score_cinema = "select * from mov_score where mov_code = {} and rep_site='cinema'"

        mov_score_cinema = cur.execute(mov_score_cinema.format(mov_code))
        mov_score_cinema = list(mov_score_cinema.fetchall())

        # NAVER
        mov_score_naver = "select * from mov_score where mov_code = {} and rep_site='naver'"

        mov_score_naver = cur.execute(mov_score_naver.format(mov_code))
        mov_score_naver = list(mov_score_naver.fetchall())

        # MEGABOX
        mov_score_mega = "select * from mov_score where mov_code = {} and rep_site='megabox'"

        mov_score_mega = cur.execute(mov_score_mega.format(mov_code))
        mov_score_mega = list(mov_score_mega.fetchall())

    url = 'http://www.kobis.or.kr/'

    return render_template('details.html', mov_info_details=mov_info_details, mov_score_cinema=mov_score_cinema,
                           mov_score_naver=mov_score_naver, mov_score_mega=mov_score_mega, url=url)

@app.route('/catalog3')
def catalog3():
    with get_db_con() as con:
        cur = con.cursor()

        mov_info_all = "select * from Mov_info"

        mov_info_all = cur.execute(mov_info_all)
        mov_info_all = list(mov_info_all.fetchall())

        url = 'http://www.kobis.or.kr/'

        total_all = 'select count(*) from mov_info'
        total_all = cur.execute(total_all)
        total_all = int(total_all.fetchone()[0])
        data_to_show=mov_info_all
        len_to_show=len(data_to_show)
        ajaxMovie=data_to_show
        return render_template('catalog3.html', url=url,len_to_show=len_to_show, data_to_show=data_to_show,ajaxMovie=ajaxMovie)


@app.route('/addMovie/<int:page>')
def getajaxMovie(page):
    with get_db_con() as con:
        cur = con.cursor()

        mov_info_all = "select * from Mov_info"

        mov_info_all = cur.execute(mov_info_all)
        mov_info_all = list(mov_info_all.fetchall())

        url = 'http://www.kobis.or.kr/'

        total_all = 'select count(*) from mov_info'
        total_all = cur.execute(total_all)
        total_all = int(total_all.fetchone()[0])
        data_to_show=mov_info_all
        ajaxMovie=data_to_show[(page-1)*12 :page*12]
        return render_template('catalog3.html', url=url, ajaxMovie=ajaxMovie)

'''
def jsonize(result):
    result_json=json.dumps(list(result.fetchall()),ensure_ascii=False).encode("utf-8")
    return result_json
'''

if __name__ == "__main__":
    app.run()
