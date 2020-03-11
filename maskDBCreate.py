import sqlite3

from sqlite3 import Error

def maskStroeDBCreate(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    
        cursor = conn.cursor()
        
        cursor.execute(f'''CREATE TABLE store (
            "code"	TEXT,
            "name"	TEXT,
            "lat"	REAL,
            "lng"	REAL,
            "remain_stat"	TEXT,
            "remain_num" Integer,
            "stock_at"	TEXT,
            "created_at"	TEXT
            )
        ''')

        conn.commit()
    
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


def userDBCreate(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    
        cursor = conn.cursor()


        # sqlite 버그 있어서 버그 회피용으로 추가된 테이블
        cursor.execute(f'''
            CREATE TABLE keyValue (
            "keyword"   TEXT    
			)
        ''')     

        # 등록된 스토어 리스트
        cursor.execute(f'''
            CREATE TABLE alert_store (
                "code" TEXT,
                "lat" REAL,
                "lng" REAL
                )
        ''')

        # 유저리스트
        cursor.execute(f'''CREATE TABLE user (
	        "deviceId"	TEXT,
            "token"     TEXT,
            "userSeq"	INTEGER PRIMARY KEY AUTOINCREMENT
            )
        ''')

        # 유저별 등록한 스토어 리스트
        cursor.execute(f'''CREATE TABLE user_alert (
            "userSeq" INTEGER,
            "code" TEXT,
            "alert" Integer,
			constraint fk_user FOREIGN KEY(userSeq) REFERENCES USER(userSeq),
            PRIMARY KEY ( userSeq, code )
            )
        ''')        
         



#        cursor.execute('''CREATE Table article
#                (id integer, title text, comment integer, category text, recommend integer, link text)
#            ''')

        # cursor.execute('''ALTER TABLE article_ppomppu
        #         ADD COLUMN column_definition
        #     ''')
        # cursor.execute('''DROP TABLE article
        #     ''')
        conn.commit()
    
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()
    pass

if __name__ == '__main__':
    DB_PATH = r'./mask.db'
    maskStroeDBCreate(DB_PATH)
    userDBCreate(DB_PATH)