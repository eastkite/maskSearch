import json
import requests
import time
from Log import log, logTrace
import sqlite3
from sqlite3 import Error

from MaskRequest import requestStore

import asyncio

DB_PATH = r'./mask.db'

def refresh_all():
    alert_store_selectSql = f"Select code, lat, lng from alert_store"

    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute(alert_store_selectSql)
        
        result = cur.fetchall()

        for x in result:
            code = x['code']
            lat = x['lat']
            lng = x['lng']
            requestStore(code, lat, lng)

    except Error as e:
        log(str(e))
        
    finally:
        if conn:
            conn.close()


if __name__ == '__main__':
    while True:
        try:
            log("parse run!!!!!!!!!!")
            refresh_all()
            time.sleep(60) 
            log("@@@@@@@@@@@@@@@@@@ all complete")
        except Exception as e:
            log('Goodbye!')
            continue

        time.sleep(60)            
