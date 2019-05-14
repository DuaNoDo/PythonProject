import sqlite3

conn = sqlite3.connect('movie.db')

c = conn.cursor()


c.execute('''CREATE TABLE movie
             (date text, trans text, symbol text, qty real, price real)''')

conn.commit()

conn.close()