from flask import Flask
from flask_restful import Resource, Api
from flask_restful import reqparse
import sqlite3
from sqlite3 import Error
from Log import log
from ProjectStaticData import as_json

class pushIDRegist(Resource):

    @as_json
    def post(self):
        DB_PATH = r'./mask.db'
        log(reqparse.request)
        parser = reqparse.RequestParser()
        parser.add_argument('deviceId', type= str)
        parser.add_argument('fcmToken', type= str)

        args = parser.parse_args()
        deviceId = args.get('deviceId')
        fcmToken = args.get('fcmToken')

        log(f'deviceId : {deviceId} , fcmToken : {fcmToken}')

        errorResponse = {
            'code' : '4001',
            'desc' : 'none parameter'
        }

        if (fcmToken is None) | (deviceId is None):
            return errorResponse

        try:
            conn = sqlite3.connect(DB_PATH)
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()


            # 있는지 먼저 체크 후 없으면 inser, 있으면 update
            insetSql = f"insert into user (token, deviceId) values (?,?)"
        
            updateSql = f"Update user set token = ? where deviceId = ?"
        
            selectSql = f"Select userSeq from user where deviceId = ?"
            cur.execute(selectSql, (deviceId,))
            row = cur.fetchone()

            data = (fcmToken, deviceId)
            if row is None:
                # 없으면
                cur.execute(insetSql, data)
                log('신규 유저등록완료')
            else:
                # 있으면
                cur.execute(updateSql, data)
                log('기존 유저 토큰 업데이트')
            
            conn.commit()               
            
            cur.execute(selectSql, (deviceId, ))
            userData = cur.fetchone()
            #log(f'userSeq : {userData['userSeq']} deviceId : {deviceId} ')
            resultData = {
                'code' : '2000',
                'desc' : "userRegistComplete",
                'result' : {
                    'seq' : userData['userSeq']
                }
            } 

            return resultData
        except Error as e:
            errorData = {
                'code' : '4040',
                'desc' : "userRegistFail"
            } 
            log(e)
            return errorData
        finally:
            if conn:
                conn.close()



