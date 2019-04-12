import sqlite3

con =sqlite3.connect('db.sqlite')

con.text_factory=str

cur=con.cursor()



cur.execute("""insert into item_info values('1','2','3')""")
con.commit()
