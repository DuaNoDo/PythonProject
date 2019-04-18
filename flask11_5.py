from flask import request
from flask import Flask
import sqlite3
import json

app=Flask(__name__)

app.debug=True

def get_db_con() ->sqlite3.connect:
    return sqlite3.connect("db.sqlite")

@app.route("/")

def hello():
    with get_db_con() as con:
        cur= con.cursor()

        q="select * from hanbit_books"
        result=cur.execute(q)

    result_json=jsonize(result)
    return result_json

@app.route("/books/by/author")

def get_books_by_author():
    name=request.args.get("name")
    with get_db_con() as con:
        cur=con.cursor()
        q="select * from hanbit_books where author like :name order by title"
        param={
            "name":"%"+name+"%"
        }
        result=cur.execute(q,param)
    result_json=jsonize(result)
    return result_json

@app.route("/books/by/month")

def get_books_by_month():
    month=request.args.get("month")
    if int(month)<10:
        month="0"+month

    with get_db_con() as con:
        cur=con.cursor()
        q="select * from hanbit_books where strftime('%m',pub_date) = :month order by pub_date desc"
        param={
            "month":month
        }
        result=cur.execute(q,param)
    result_json=jsonize(result)
    return result_json

def jsonize(result):
    result_json=json.dumps(list(result.fetchall()),ensure_ascii=False).encode("utf-8")
    return result_json

if __name__=="__main__":
    app.run()

