
import sqlite3
from sqlite3 import Error
from Log import log
import time
import ProjectStaticData

def refreshData():
    DB_PATH = ProjectStaticData.DB_PATH
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        selectKeyword = f"select code, lat, lng from alert_store"
        cur.execute(selectKeyword)

        storeList = {}
        for item in cur.fetchall():
            storeList[item['code']] = item['code']
        
        log(storeList)

    except Exception as e:
        log(e)
    finally:
        if conn:
            conn.close

