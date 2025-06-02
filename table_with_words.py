import sqlite3 as sql
import config

class TableWords:
    def __init__(self):
        base = sql.connect(config.PATH_TO_DATABASE)
        curs = base.cursor()
        curs.execute('''CREATE TABLE IF NOT EXISTS AllWords (Word TEXT, Translate TEXT)''')
        base.commit()
        base.close()

    def add_notice(self, word, translate):
        base = sql.connect(config.PATH_TO_DATABASE)
        curs = base.cursor()
        curs.execute('''INSERT INTO AllWords (Word, Translate) VALUES (?, ?)''', (word, translate))
        base.commit()
        base.close()

    def read_table(self):
        base = sql.connect(config.PATH_TO_DATABASE)
        curs = base.cursor()
        curs.execute('''SELECT Word FROM AllWords''')  
        list_words = curs.fetchall()
        words = []
        for item in list_words:
            words.append(item[0])     
        base.close()
        return words   

    def read_string(self, word):
        base = sql.connect(config.PATH_TO_DATABASE)
        curs = base.cursor()
        curs.execute('''SELECT Translate FROM AllWords WHERE Word == ?''', (word,))      
        translate = curs.fetchone()[0]  
        base.close()  
        return translate
    



