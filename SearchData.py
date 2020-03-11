from flask import Flask, request
from flask_restful import Resource, Api
from flask_restful import reqparse
import sqlite3
from sqlite3 import Error
from Log import log

from ProjectStaticData import as_json

class Search(Resource):

    @as_json
    def get(self):
        from ProjectStaticData import preference as PRE
        log(reqparse.request)    

        parser = reqparse.RequestParser()
        parser.add_argument('key', type = str)
        parser.add_argument('count', type = int)
        parser.add_argument('containEnd', type = int)

        args = parser.parse_args()
        searchKeyword = args.get('key')

        log(args)
        containEnd = args['containEnd']

        limitCount = args.get('count')
        if limitCount is None:
            limitCount = 50

        sites = PRE.SITES
        dataList = []
        try:
            for name, info in iter(PRE.SITES.items()):
                tab = info['table']

                conn = sqlite3.connect(PRE.DB_PATH)
                conn.row_factory = sqlite3.Row
                cur = conn.cursor()
                if searchKeyword :
                    if containEnd == 0:
                        # 종료 딜 미포함
                        sql = f"SELECT * from {tab} WHERE title like '%{searchKeyword}%' and articleEnd == 0 ORDER By id Desc LIMIT {limitCount}"
                    else :
                        # 종료 딜 포함
                        sql = f"SELECT * from {tab} WHERE title like '%{searchKeyword}%' ORDER By id Desc LIMIT {limitCount}"
                else :
                    return { 
                        'code' : '4010',  
                        'result' : {                        
                            'desc' : "HTTP-401 param didn't define" }
                            }
                log(sql)

                cur.execute(sql)
                rows = cur.fetchall()
                
                for x in rows:
                    dataList.append({
                                    'siteId' : info['id'],
                                    'siteIcon' : info['icon'],
                                    'articleId': x['id'],
                                    'title': x['title'],
                                    'comment': x['comment'],
                                    'category' : x['category'],
                                    'recommend' : x['recommend'],
                                    'decommend': x['decommend'],
                                    'url' : x['link'],
                                    'articleEnd' : x['articleEnd'],
                                    'thumbnail': x['thumbnail'],
                                    'regDate' : f"{x['regDay']} {x['regTime']}"
                                    })
                             
        except Exception as e:
            # errorCode-4100 : db 데이터 비 정상
            resultData =  { 
                    'code' : '4041',  
                    'result' : {                        
                        'desc' : "HTTP-404 dbData don't have data" }
                        }
            log((str(e), '\n', resultData))
            return resultData
        finally:
            if conn:
                conn.close()


        if len(dataList) == 0:
            return {
                'code' : '4045',
                'result' : {
                    'desc' : 'HTTP-404 none data'
                }
            }


        return { 
                'code' : '2000',  
                'result' : dataList
                }