import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from Matching.messagesender import *

# app.py 작성시 맨 아래쪽의 Method(app.py) 부분 참고
# messageSender 부분 수정 필요(requireMatching)

# messageSender 객체 생성
messageSender = MessageSender()

##### PD Layer Class #####
class Matching:
    # Super Class
    def __init__(self, matchingIdx: int, success: bool, helpee: UserCommonInfo, helper: UserCommonInfo, reqDate: str,
                 address: Address):
        self.__matchingIdx = matchingIdx
        self.__requestDate = reqDate
        self.__address = address

        self.__matchingSuccess = success
        self.__matchedHelpeeInfo = helpee
        self.__matchedHelperInfo = helper

    def requireMatching(self, helper: UserCommonInfo):
        pass

    def delete():
        pass

    # Matching Getter
    def getMatchingIdx(self):
        return self.__matchingIdx

    def getMatchingSuccess(self):
        return self.__matchingSuccess

    def getRequestDate(self):
        return self.__requestDate

    def getAddress(self):
        return self.__address

    def getHelperInfo(self):
        return self.__matchedHelperInfo

    def getHelpeeInfo(self):
        return self.__matchedHelpeeInfo


# Accompany (병원 동행)
class Accompany(Matching):
    # 초기화: 매칭번호, 매칭완료여부, 헬피userInfo, 헬퍼userInfo, 주소, 병원주소, 동행이유
    def __init__(self, matchingIdx: int, success: bool, helpee: UserCommonInfo, helper: UserCommonInfo, reqDate: str,
                 address: Address, hospitalLocation: Address, reason: str):
        self.__matchingIdx = matchingIdx
        self.__requestDate = reqDate
        self.__address = address
        self.__hospitalLocation = hospitalLocation
        self.__reason = reason

        self.__matchingSuccess = success
        self.__matchedHelpeeInfo = helpee
        self.__matchedHelperInfo = helper

    def requireMatching(self, helper: UserCommonInfo):
        self.__matchingSuccess = True
        self.__matchedHelperInfo = helper
        messageSender.sendMatching(self, self.getHelperInfo(), self.getHelpeeInfo(), "병원 동행")

    def update(self, reqDate: str, address: Address, hospitalLoc: Address, reason: str):
        self.__requestDate = reqDate
        self.__address = address
        self.__hospitalLocation = hospitalLoc
        self.__reason = reason

        self.__matchedHelpeeInfo = DB_getUser(self.__matchedHelpeeInfo.ID).getUserInfo()

    def delete(self):
        deleteMatching(self.__matchingIdx)

    # Accompany Getter
    def getMatchingIdx(self):
        return self.__matchingIdx

    def getMatchingSuccess(self):
        return self.__matchingSuccess

    def getRequestDate(self):
        return self.__requestDate

    def getAddress(self):
        return self.__address

    def getHospitalLocation(self):
        return self.__hospitalLocation

    def getReason(self):
        return self.__reason

    def getHelperInfo(self):
        return self.__matchedHelperInfo

    def getHelpeeInfo(self):
        return self.__matchedHelpeeInfo


class Counsel(Matching):
    # 초기화: 매칭번호, 매칭완료여부, 헬피userInfo, 헬퍼userInfo, 요청날짜(+시간), 주소, 상담유형
    def __init__(self, matchingIdx: int, success: bool, helpee: UserCommonInfo, helper: UserCommonInfo, reqDate: str,
                 address: Address, category: str):
        self.__matchingIdx = matchingIdx
        self.__requestDate = reqDate
        self.__address = address
        self.__category = category

        self.__matchingSuccess = success
        self.__matchedHelpeeInfo = helpee
        self.__matchedHelperInfo = helper

    def requireMatching(self, helper: UserCommonInfo):
        self.__matchingSuccess = True
        self.__matchedHelperInfo = helper
        messageSender.sendMatching(self, self.getHelperInfo(), self.getHelpeeInfo(), "심리 상담")
        # MessageSender.sendAppointment(self, helper.getUserInfo(), helpee.getUserInfo(), "심리 상담")

    def update(self, reqDate: str, address: Address, category: str):
        self.__requestDate = reqDate
        self.__address = address
        self.__category = category

        self.__matchedHelpeeInfo = DB_getUser(self.__matchedHelpeeInfo.ID).getUserInfo()

    def delete(self):
        deleteMatching(self.__matchingIdx)

    # Counsel Getter
    def getMatchingIdx(self):
        return self.__matchingIdx

    def getMatchingSuccess(self):
        return self.__matchingSuccess

    def getRequestDate(self):
        return self.__requestDate

    def getAddress(self):
        return self.__address

    def getCategory(self):
        return self.__category

    def getHelperInfo(self):
        return self.__matchedHelperInfo

    def getHelpeeInfo(self):
        return self.__matchedHelpeeInfo


class SafetyCheck(Matching):
    # 초기화: 매칭번호, 매칭완료여부, 헬피userInfo, 헬퍼userInfo, 요청날짜(+시간), 주소, 점검부분
    def __init__(self, matchingIdx: int, success: bool, helpee: UserCommonInfo, helper: UserCommonInfo, reqDate: str,
                 address: Address, checkPart: str):
        self.__matchingIdx = matchingIdx
        self.__requestDate = reqDate
        self.__address = address
        self.__checkPart = checkPart

        self.__matchingSuccess = success
        self.__matchedHelpeeInfo = helpee
        self.__matchedHelperInfo = helper

    def requireMatching(self, helper: UserCommonInfo):
        self.__matchingSuccess = True
        self.__matchedHelperInfo = helper
        messageSender.sendMatching(self, self.getHelperInfo(), self.getHelpeeInfo(), "안전 점검")
        # MessageSender.sendAppointment(self, helper.getUserInfo(), helpee.getUserInfo(), "안전 점검")

    def update(self, reqDate: str, address: Address, checkPart: str):
        self.__requestDate = reqDate
        self.__address = address
        self.__checkPart = checkPart

        self.__matchedHelpeeInfo = DB_getUser(self.__matchedHelpeeInfo.ID).getUserInfo()

    def delete(self):
        deleteMatching(self.__matchingIdx)

    # Counsel Getter
    def getMatchingIdx(self):
        return self.__matchingIdx

    def getMatchingSuccess(self):
        return self.__matchingSuccess

    def getRequestDate(self):
        return self.__requestDate

    def getAddress(self):
        return self.__address

    def getCheckPart(self):
        return self.__checkPart

    def getHelperInfo(self):
        return self.__matchedHelperInfo

    def getHelpeeInfo(self):
        return self.__matchedHelpeeInfo