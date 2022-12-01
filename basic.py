import requests

service_key = 'devU01TX0FVVEgyMDIyMTEyNjExNDQxMzExMzI2MTA='

class Address:
    detailAddress:str     # 도로명주소 전체
    placeName:str   # 건물명
    region:str      # 시도명

    def __init__(self, detailAddress:str, placeName:str, region:str):
        self.detailAddress = detailAddress
        self.placeName = placeName
        self.region = region

# 주소 받아오기 / ret: Address
def getAddress():
    pass