import sqlite3

class tt_twitter:

    def __init__(self):
        self.con = sqlite3.connect("database.db")
        self.cur = self.con.cursor()
        self.create_table()

    def create_table(self):
        #self.cur.execute("""DROP TABLE tt_twitter""")
        self.cur.execute("""CREATE TABLE IF NOT EXISTS tt_twitter (
        top INTEGER,
        tittles TEXT,
        twitts INTEGER,
        date TEXT,
        time TEXT
        )""")

    def insert(self,item):
        self.cur.execute("""INSERT OR IGNORE INTO tt_twitter VALUES(?,?,?,?,?)""",item)
        self.con.commit()

    def read(self):
        self.cur.execute("""SELECT * FROM tt_twitter""")
        rows = self.cur.fetchall()
        return rows


