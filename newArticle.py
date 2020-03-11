
import sqlite3
from sqlite3 import Error
from Log import log
import time
from ProjectStaticData import preference as PRE

from pushService import pushSend

def newArticle():
    try:
        conn = sqlite3.connect(PRE.DB_PATH)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        selectKeyword = f"select keyword, keySeq from keyword "
        cur.execute(selectKeyword)

        keywordList = {}
        for item in cur.fetchall():
            keywordList[item['keySeq']] = item['keyword']
        
        # log(keywordList)

    except Exception as e:
        log(e)
    finally:
        if conn:
            conn.close

    alertList = []
    for name, info in iter(PRE.SITES.items()):
        dbName = "new_" + PRE.TAB[name]
        selectSql = f"select id, title, link from {dbName} where isFirst == 0"
        updateSql = f"update {dbName} set isFirst = 1 where id = (?)"

        try:
           

            conn = sqlite3.connect(PRE.DB_PATH)
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute(selectSql)
            
            for article in cur.fetchall():
                log(f"{article['id']}, {article['title']}, {article['link']}")
                title = article['title']
                for seq, keyword in keywordList.items():                
                    if ((title.replace(" ", "")).upper()).find(keyword.replace(" ", "").upper()) != -1:
                        log(f"포함하는 키워드 {seq} : {keyword}")
                        alertList.append({"articleId" : article['id'], "link" : article['link'], "title": title, "keySeq": seq, "keyword" : keyword, "site" : info['id']})

                
                cur.execute(updateSql, (article['id'], ))    

            conn.commit()
        except Exception as e:
            log(e)
        finally:
            if conn:
                conn.close()
    
    alertNewArticle(alertList)

def alertNewArticle(list):
    log("alertNewArticle")

    pushService = pushSend()
    # selectSql = "select userSeq from keyword_alert where alert == 1 AND keySeq = (?)"
    # userSelect = "select token from user where userSeq = (?)"
    pushList = {}
    try:
        conn = sqlite3.connect(PRE.DB_PATH)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        
        # for item in list:
        #     keySeq = item['keySeq']
        #     cur.execute(selectSql, (keySeq, ))
        #     for user in cur.fetchall():
        #         pushList[(user['userSeq'], item['articleId'])] = {"title" : item['title'], "link" : item['link'],  "keyword" : item['keyword']}

        for pushData in list:
            # userSeq = seq[0]
            # cur.execute(userSelect, (userSeq, ))
            title = f"[ 키워드 알림 : {pushData['keyword']} ]"
            body =  f"{pushData['title']}"
            data = {
                "link" : pushData['link'],
                'code' : 'link_landing',
                'site' : pushData['site'],
                'articleId' : pushData['articleId']
            }
            # token = cur.fetchone()['token']
            utfData = pushData['keyword'].encode('utf-8')
            topic = ["%" + str(hex(c))[2:].upper() for c in utfData]
            finalTopic = ""
            for c in topic: 
                finalTopic = finalTopic + c
            
            token = f"/topics/{finalTopic}"

            pushService.send_fcm_notification(token, title, body, data)

    except Exception as e:
        log(e)
    finally:
        if conn:
            conn.close()



if __name__ == '__main__':
    while True:
        try:        
            log("new Article run!!!!!!!!!!")
            newArticle()
            log("@@@@@@@@@@@@@@@@@@ all complete")
            
        except KeyboardInterrupt:
            log('Goodbye!')

        time.sleep(60)            

