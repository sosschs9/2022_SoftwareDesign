import datetime

class HelperType:
    ACCOMPANY = 1
    COUNSEL = 2
    SAFETYCHECK = 4

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

# DB 불러올 때 변환용
def data_to_UserInfo(result:dict, indexHead:str):
    return UserCommonInfo(result[indexHead]['ID'], result[indexHead]['NAME'], result[indexHead]['PHONENUMBER'], result[indexHead]['GENDER'])
def data_to_Address(result:dict, indexHead:str):
    return Address(result[indexHead]['detailAddress'], result[indexHead]['placeName'], result[indexHead]['region'])