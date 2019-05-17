import sqlite3

conn = sqlite3.connect('movie.db')

c = conn.cursor()

cr_mov_info='''CREATE TABLE IF NOT EXISTS Mov_info(
            Mov_name_kor text,
            Mov_name_eng text,
            Mov_date text,
            Mov_category text,
            Mov_nation text,
            Mov_age text,
            Mov_director text,
            Mov_actor text,
            Mov_content text,
            Mov_img text,
            primary key(Mov_name_kor,Mov_date));'''
c.execute(cr_mov_info)

conn.commit()

cr_mov_score='''CREATE TABLE IF NOT EXISTS Mov_score(
            Mov_score_name_kor text,
            Mov_score_date text,
            Mov_score_score real,
            Mov_score_reple text,
            Mov_score_site text,
            primary key(Mov_score_name_kor,Mov_score_date),
            foreign key(Mov_score_name_kor) references Mov_info(Mov_name_kor),
            foreign key(Mov_score_date) references Mov_info(Mov_date);'''
c.execute(cr_mov_score)

conn.commit()

conn.close()