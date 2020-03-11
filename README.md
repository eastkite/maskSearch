
# Hotdeal-Crawling-Server
## 핫딜 리스트 크롤링하여 db 구축 및 서버 조회하기 위한 저장소

언어 : python
사용라이브러리 :  
    db        - sqlite3
    server    - Flask
    
##### 첫 커밋 날자 : 2019-12-09

#### 아래 명령어 사용하여 환경 설정 
    pip3 install -r requirements.txt


## 현재 지원하는 사이트 
    - 뽐뿌 (0)
    - 클리앙 (1)

## 지원 예정 사이트
    - 루리웹
    - 기타..


#### API 
    - (get) hotdeal/list : 
        지원하는 리스트 배열 형태로 제공 

        request : none

        response : 배열
        [
        'id' : integer
        'name' : String
        ]

    - (get) hotdeal : 
        제공을 원하는 db 아이디를 request에 넣으면 20개 씩 데이터 response
        id 값을 넣어서 보내면 id 이하의 20개 데이터 response

        request : 
            dbTableIndex : Int
            {id : Int}
        
        response : 배열
        [
            'articleId'  : Int 
            'title'      : String
            'comment'    : Int 
            'category'   : String 
            'recommend'  : Int
            'decommend'  : Int
            'url'        : String 
            'articleEnd' : Int (0/1 Bool) 
            'thumbnail'  : String 
            'regDate'    : String (yyyy-MM-dd HH:mm:SS Date) 
        ]
        
    - (post) user/registId :
        현재 사용자의 uuid(device ID)와 fcm 토큰을 등록하고, 현재 유저의 시퀀스 및 저장되어있는 추천, 코멘트 알림 정보를 가져온다
        # 추천, 코멘트 알림 정보 TBD
        request :
            deviceId : String
            fcmToken : String
        
        response :
            "seq" : Int,
            "comment" : Int,
            "recommend" : Int,

    - (post) user/keyword :
        원하는 키워드를 등록하여 알림을 받기 위한 용도

        request :
            seq : Int (유저 시퀀스)
            keyword : String

        response : 
            none

    - (get) user/keyword :
        현재 유저의 등록된 키워드를 가져온다
        해당 키워드의 알림을 0/1로 표현

        request : 
            userSeq : Int

        response : 배열
            keyword : String
            alert : Int (0/1)
    
    - (put) user/keyword :
        등록 되어있는 키워드의 알림을 헤재한다

        request :
            userSeq : Int
            keyword : String
            alert : Int (0/1)

        response :
            none

    - (delete) user/keyword :
        등록 되어있는 키워드를 삭제 한다.
        
        request :
            userSeq : Int
            keyword : String
        
        response :
            none



## 소스 간단 설명
 - 기본 소스
    - dbCreate.py -
	DB 및 테이블 생성
    - projectStaticData.py -
	공통적으로 사용할 수 있는 부분 모음(table명, db_path 등)
    - pushService.py -
	푸시보내기 위한 간단 서비스

 - 크롤링
    - selectDB -
	id로 db 탐색하여 이미 있는 지 여부 확인

    - dbDataInsert.py -
	selectDB 결과값에 따라 row 추가 또는 update sql 실행

    - parsers.py -
	각 함수별로 butifulsoup4 사용하여 필요 데이터 파싱
	get_soup(url) : html 소스 받아와서 parse

    - run.py -
	parsers 를 실행하고 계속 유지하기위한 소스
	

 - API
    - DBListSelect.py -
	현재 파싱을 하고있는 리스트 제공을 위한 get함수 구현

    - ppompuSelectData.py -
	파일이름이 ppomppu이긴 하나,, 모든 사이트 대상으로 데이터를 제공하기위한 get 구현

    - keywordRegist.py -
	keyword관련한 API method 4가지 모두 구현(get, post, delete, put)

    - pushRegist.py -
	User정보 post 및 userSeq 전달

    - ServerRun.py -
	서버 구동. 안에 위 4개 파일을 import 하고, url 연결

 - KeyWord 검색
     - newArticle.py -
	새로운 게시글이 올라왔을 때 키워드를 전부 가져와서 포함하고 있는지 확인 후 푸시 전송

