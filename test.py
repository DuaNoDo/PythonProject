from flask import Flask, render_template, redirect, request, url_for
import sqlite3
import json

app = Flask(__name__)

app.debug = True


@app.route('/',methods = ['POST', 'GET'])
@app.route('/<int:num>')
def inputTest(num=None):
    return render_template('test.html', num=num)


@app.route('/calculate', methods=['POST'])
def calculate(num=None):
    if request.method == 'POST':
        temp = request.form['num']
    else:
        temp = None
    return redirect(url_for('test', num=temp))


if __name__ == '__main__':
    app.run()

