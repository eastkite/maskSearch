import requests
import json
from Log import log

class pushSend(object):
    
    def send_fcm_notification(self, ids, title, body, data):
        log(f"{ids},{title}, {body}, {data}")
        # fcm 푸시 메세지 요청 주소
        url = 'https://fcm.googleapis.com/fcm/send'
        
        # 인증 정보(서버 키)를 헤더에 담아 전달
        headers = {
            'Authorization': 'key=AAAAqXiHCc8:APA91bG4e3EziToT1lyD1RifljyBTOmTdi1PJ4Lqq5OYWqlq-Dwr8i8Q5Ca4ho8XdRzicorNgGivm8togjBMgitOHEMW3y9UA0sq6Tv-snuq2DDJOt6_T54Uaju5Qmtwn3uGHDngIt1C',
            'Content-Type': 'application/json; UTF-8',
        }
        
        data['title'] = title
        data['body'] = body

        # 보낼 내용과 대상을 지정
        content = {
            'to': ids,
            'notification': {
            "sound" : "default",
            'title': title,
            'body': body,
            "content_available": True
            },
            'data': data,
            "priority": "high"
        }

        # json 파싱 후 requests 모듈로 FCM 서버에 요청
        response = requests.post(url, data=json.dumps(content), headers=headers)
        print(response.json)


if __name__ == '__main__':
    pushService = pushSend()
    data = {
        'link' : 'http://www.naver.com',
        'code' : 'link_landing'
    }
    utfData = "안녕하세요".encode('utf-8')
    topic = ["%" + str(hex(c))[2:].upper() for c in utfData]
    finalTopic = ""
    for c in topic: 
        finalTopic = finalTopic + c
    pushService.send_fcm_notification(f'/topics/{finalTopic}',"hi","test", data)