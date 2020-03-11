
from datetime import datetime
import enum
import locale

def log(logData):
    locale.setlocale(locale.LC_ALL, 'Ko_kr')
    print(f"[{datetime.now()}] : {logData}")



        # 
        # # 현재 시간 
        # print(datetime.now().strftime("%Y.%b.%d %H:%M:%S"))

def logTrace():
    locale.setlocale(locale.LC_ALL, 'Ko_kr')
    print(f"[{datetime.now()}")