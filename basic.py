import requests
import datetime

class UserCommonInfo:
    def __init__(self, id:str, name:str, phoneNumber:str, gender:bool):
        self.ID = id
        self.NAME = name
        self.PHONENUMBER = phoneNumber
        self.GENDER = gender

class Address:
    detailAddress:str     # 도로명주소 전체
    placeName:str   # 건물명
    region:str      # 시도명

    def __init__(self, detailAddress:str, placeName:str, region:str):
        self.detailAddress = detailAddress
        self.placeName = placeName
        self.region = region 

# 현재 시간 > str / ret:str
def getNowTime():
    return datetime.datetime.now().strftime('%y.%m.%d')