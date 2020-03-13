import json
import requests
import sqlite3
from sqlite3 import Error
from Log import log
from pushService import pushSend

def requestStore(storeId, lat, lng):
    url = "https://8oi9s0nnth.apigw.ntruss.com/corona19-masks/v1/storesByGeo/json"
    param = {'lat' : lat, 'lng': lng, 'm': 10}
    
    response = requests.get(url=url, params = param)
    # print(f'{response.json()}'.replace('\'', '\"'))
    js = f"{response.json()}".replace('\'', '\"').replace('None','null')
    log(js)
    correctStore = jsonDecoder(js, storeId)
    if correctStore is not None:
        # 일치하는 상점이 있으면
        # TODO: 일치하는 상점의 db 정보 조회하여 해당 정보와 비교하는 함수 필요
        log("일치 하는 항목이 있네요")
        code = correctStore['code']
        if hadStoreInfo(code):
            log("이미 상점 정보를 갖고 있어요")
            data = selectSpecificStore(code)
            remain = correctStore["remain_stat"]
            log(data)
            log(data['remain_num'])
            if remain == "planty":
                remain_num = 4
            elif remain == "some":
                remain_num = 3
            elif remain == "few":
                remain_num = 2
            elif remain == "empty":
                remain_num = 1
            else:
                remain_num = 0

            # if remain_num == 1 and int(data['remain_num']) != 1:
            #     pushWithTopic(correctStore, "[마스크 알림]", f"등록하신 {data['name']} 에 마스크가 품절 되었어요.")
            #     # 품절
            #     pass

            if int(data['remain_num']) < remain_num:
                # 해당 상점의 마스크 수가 늘어났다
                if remain_num > 1:
                    pushWithTopic(correctStore, "[마스크 알림]", f"등록하신 {data['name']} 에 마스크가 들어왔어요.")

            # elif int(data['remain_num']) > remain_num:
            #     pushWithTopic(data, "[마스크 알림]", f"등록하신 {data['name']} 에 마스크가 줄어들고 있어요.")
            #     # 줄어들고있어요
            #     pass
            updateStoreInfo(correctStore)
        else:
            # 상점이 없으니 신규 저장
            log("상점 정보가 없어요 새로 저장합니다.")
            insertStoreInfo(correctStore)        

        pass
    else:
        # 일치하는 상점이 없으면
        # 뭐하지?
        log("일치 안하네요")
        pass

def pushWithTopic(store, title, body):
    pushService = pushSend()

    token = f"/topics/{store['code']}"

    pushService.send_fcm_notification(token, title, body, store)

# 해당 코드로 상점이 DB에 존재하는지 조회
def hadStoreInfo(code):
    store_selectSql = f"Select code from store where code = {code}"

    DB_PATH = r'./mask.db'

    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        cur.execute(store_selectSql)
        
        data = cur.fetchone()
        log(f"hadStore : {data}")
        if data is None:
            return False
        else:
            return True
 
    except Error as e:
        log((str(e)))
    finally:
        if conn:
            conn.close()

# 특정 상점 정보 DB 조회 hadStroeInfo 선행 후 True 면 실행
def selectSpecificStore(code):
    store_selectSql = f"Select * from store where code = {code}"

    DB_PATH = r'./mask.db'

    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        cur.execute(store_selectSql)
        
        data = cur.fetchone()
        
        if data is not None:
            resultData = {
                'code' : data['code'],
                'name' : data['name'],
                'lat' : data['lat'],
                'lng' : data['lng'],
                'remain_stat' : data['remain_stat'],
                'stock_at' : data['stock_at'],
                'created_at' : data['created_at'],
                'remain_num' : data['remain_num']
            }
            log(f"resultData : {resultData}")
            return resultData        
 
    except Error as e:
        log((str(e)))
    finally:
        if conn:
            conn.close()

# 상점 정보 저장
def insertStoreInfo(data):
    store_insertSql = f"insert into store (code, name, lat, lng, remain_stat, stock_at, created_at, remain_num) values(?,?,?,?,?,?,?,?)"

    DB_PATH = r'./mask.db'

    try:
        log("저장 했니?")
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        cur.execute(store_insertSql, (data['code'], data['name'], data["lat"], data["lng"], data["remain_stat"], data["stock_at"], data["created_at"], data["remain_num"]))
        log("저장 완료?")
        conn.commit()
        log("커밋 완료?")
        return True
 
    except Error as e:
        log((str(e)))
        return False
    finally:
        if conn:
            conn.close()

# 상점 정보 업데이트
def updateStoreInfo(data):
    store_updateSql = f"update store set remain_stat = ?, stock_at = ?, created_at = ?, remain_num = ? where code = ?"

    DB_PATH = r'./mask.db'

    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        cur.execute(store_updateSql, (data['remain_stat'], data['stock_at'], data['created_at'], data['remain_num'], data['code']))
        
        log("업데이트 완료?")
        conn.commit()

        return True
 
    except Error as e:
        log((str(e)))
        return False
    finally:
        if conn:
            conn.close()

def jsonDecoder(jsonLoad, storeId):
    dic = json.loads(jsonLoad)
    # print(dic)

    # print(dic["stores"])    
    stores = dic["stores"]
    for s in stores:
        remain = s["remain_stat"]

        if remain == "planty":
            remain_num = 4
        elif remain == "some":
            remain_num = 3
        elif remain == "few":
            remain_num = 2
        elif remain == "empty":
            remain_num = 1
        else:
            remain_num = 0

        data = {
            "code" : s["code"],
            "name" : s["name"],
            "lat" : s["lat"],
            "lng" : s["lng"],
            "remain_stat" : s["remain_stat"],
            "stock_at" : s["stock_at"],
            "created_at" : s["created_at"],
            "remain_num" : remain_num
        }

        if s['code'] == storeId:
            return data



if __name__ == '__main__':
    # requestStore("41819012", 37.3899764, 126.953531)
    # jsonString = '{ "count": 2, "stores":[{"addr" : "경기도 고양시 덕양구 무원로 63, 103호 (행신동, 무원마을10단지아파트)","code": "31811787","created_at": "2020/03/11 10:40:00","lat": 37.6184485, "lng": 126.8305345, "name": "메디팜행신약국", "remain_stat": "empty","stock_at": "2020/03/10 10:45:00", "type": "01"}]}'
    # data = "{'code': '11889217', 'name': '대명약국', 'lat': 37.4814002, 'lng': 126.8837813, 'remain_stat': 'empty', 'stock_at': '2020/03/13 10:25:00', 'created_at': '2020/03/13 13:50:00', 'remain_num': 1}"
    
    # jsonDecoder(jsonString, "41819012")
    # pushWithTopic(data, "[마스크 알림]", f"등록하신 {data['name']} 에 마스크가 들어왔어요.")
    pass

