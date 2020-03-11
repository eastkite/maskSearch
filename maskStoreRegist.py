from flask import Flask
from flask_restful import Resource, Api
from flask_restful import reqparse
import sqlite3
from sqlite3 import Error
from Log import log
from MaskRequest import *

DB_PATH = r'./mask.db'

class store(Resource):    
    
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('userSeq', type= int)
        parser.add_argument('code', type= str)

        args = parser.parse_args()
        userSeq = args.get('userSeq')
        code = args.get('code')
        
        errorResponse = {
            'code' : '4001',
            'desc' : 'none parameter'
        }

        if (userSeq is None) | (code is None):
            return errorResponse

        try:
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()

            requestDeleteRow = f'''DELETE from user_alert WHERE code = (?) and userSeq = (?)'''
            
            cur.execute(requestDeleteRow, (code, userSeq))
            
            conn.commit()

            selectRow = f''' select * from user_alert where code = {code} '''

            cur.execute(selectRow)

            if cur.fetchone() is None:
                storeDeleteRow = "DELETE from store WHERE code = (?)"
                cur.execute(storeDeleteRow, (code, ))
                storeDeleteRow = "DELETE from alert_store WHERE code = (?)"
                cur.execute(storeDeleteRow, (code, ))
                conn.commit()

            resultData = {
                'code' : '2000',
                'desc' : "alert coluom delete complete",
                'result' : {}
            } 

            return resultData
        except Error as e:
            resultData =  { 
                    'code' : '4041',  
                    'desc' : "HTTP-404 dbData don't have data"}
            log((str(e), '\n', resultData))
            return resultData
        finally:
            if conn:
                conn.close()

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('userSeq', type= int)
        args = parser.parse_args()
        userSeq = args.get('userSeq')
        
        errorResponse = {
            'code' : '4001',
            'desc' : 'none parameter'
        }

        if (userSeq is None):
            return errorResponse

        try:
            conn = sqlite3.connect(DB_PATH)
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()            

            requestUserHadCode = f'''
            select code, alert from user_alert where userSeq = (?)
            '''
            cur.execute(requestUserHadCode, (userSeq,))
            
            data = []
            for row in cur.fetchall():
                # data.append(row['code'])

                storeDataSql = f'''
                select * from store where code = (?)
                '''
                cur.execute(storeDataSql, (row['code'], ))
                
                curData = cur.fetchone()
                if curData is not None:
                    log(f"curData : {curData}")
                    data.append(curData)
            
            storeList = []
            
            for info in data:
                code = info['code']
                log(f"{code}")
                if hadStoreInfo(code):
                    storeList.append(selectSpecificStore(code))

            resultData = {
                'code' : '2000',
                'desc' : "user code list get",
                'result' : storeList
            } 

            return resultData
        except Error as e:
             # errorCode-4041 : db 데이터 비 정상
            resultData =  { 
                    'code' : '4041', 
                    'desc' : "HTTP-404 dbData don't have data"}
            return resultData
        finally:
            if conn:
                conn.close()


    def post(self):
        log(reqparse.request)        
        parser = reqparse.RequestParser()
        parser.add_argument('userSeq', type= int)
        parser.add_argument('code',type= str)
        parser.add_argument('lng',type= float)
        parser.add_argument('lat', type= float)

        args = parser.parse_args()
        lat = args.get('lat')
        lng = args.get('lng')
        code = args.get('code')
        userSeq = args.get('userSeq')

        print(args)

        errorResponse = {
            'code' : '4001',
            'desc' : 'none parameter'
        }

        if (userSeq is None) or (code is None) or (lat is None) or (lng is None):
            return errorResponse

        isFirst = False

        try:
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()

            # 한사람당 등록할 수 있는 키워드 갯수 10개로 제한
            limit_selectSql = f"select count(code) from user_alert where userSeq = (?)"
            cur.execute(limit_selectSql, (userSeq,))
            count = cur.fetchone()[0]
            log(count)
            
            log(f'user : {userSeq} - registCount : {count}')
            if count == 10 :
                resultData = { 
                    'code' : '4002',  
                    'desc' : "userData over code"
                }            
                return resultData


            # 있는지 먼저 체크 후 없으면 insert, 있으면 update?
            # 이미 등록된 약국인지 체크
            alert_store_selectSql = f"Select code from alert_store where code = ?"

            # alert_store에 약국 등록
            alert_store_insetSql = f"insert into alert_store (code, lat, lng) values (?,?,?)"

            # 알림에 등록
            user_alert_insertSql = f"insert into user_alert (code, userSeq, alert) values (?,?,?)"

            cur.execute(alert_store_selectSql, (code, ))
            currentSeq = cur.fetchone()
            log(currentSeq)
            if currentSeq:
                # 있으면 
                log(currentSeq[0])
                cur.execute(user_alert_insertSql, (currentSeq[0], userSeq, 1))
            else:
                # 없으면
                cur.execute(alert_store_insetSql, (code, lat, lng))
                cur.execute(user_alert_insertSql, (code, userSeq, 1))
                isFirst = True
                

            conn.commit()
            log('code regist commit complete')

            resultData = {
                'code' : '2000',
                'desc' : "codeRegistComplete",
                'result' : {}
            } 

            return resultData
        except Error as e:
            # errorCode-4041 : db 데이터 비 정상
            resultData =  { 
                    'code' : '4041',  
                    'desc' : "HTTP-404 dbData don't have data"
            }            
            
            if e.args[0] == 'UNIQUE constraint failed: user_alert.userSeq, user_alert.code':
                resultData['code'] = '4042'
                resultData['desc'] = 'already regist alert code'
                log('result change')

            log((str(e), '\n', resultData))
            return resultData
        finally:
            if conn:
                conn.close()
            if isFirst:
                requestStore(code, lat, lng)

            

        
