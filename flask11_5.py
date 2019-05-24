from flask import Flask, render_template, redirect, request, url_for
import sqlite3
import json

app=Flask(__name__)

app.debug=True

def get_db_con() ->sqlite3.connect:
    return sqlite3.connect("movie.db")

@app.route("/")
def index():

    with get_db_con() as con:
        cur= con.cursor()

        q = "select * from Mov_info"

        result = cur.execute(q)
        result2 = list(result.fetchall())

        url = "http://www.kobis.or.kr/kobis/business/mast/mvie/popupImg.do?imgURL="

    return render_template('index.html',result=result2, url=url)





'''
def jsonize(result):
    result_json=json.dumps(list(result.fetchall()),ensure_ascii=False).encode("utf-8")
    return result_json
'''
if __name__=="__main__":
    app.run()

