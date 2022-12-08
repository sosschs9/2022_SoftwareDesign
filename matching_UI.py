from matching import *
from user import *

##### Method(app.py) #####
# Matching 불러오기 >> getMatching(matchingIdx:int)
# 매칭 페이지 수 >> getAllPostPageCount(helpType:int)
# 매칭 목록 불러오기 >> getMatchingList(pageNumber:int, helpType:int)
# 유저 매칭요청 목록 불러오기 >> getUserRequestList(postNumList:list)
# 유저(도우미) 매칭 목록 불러오기 >> getUserHelpList(postNumList:list)

# 새로운 매칭(병원동행) 생성 :: 헬피ID, 요청날짜, 주소, 병원주소, 동행이유
def createAccompany(helpeeID: str, reqDate: str, address: Address, hospitalLoc: Address, reason: str):
    user = DB_getUser(helpeeID)
    userInfo = user.getUserInfo()
    matchingIdx = getMatchingNumber()

    matching = Accompany(matchingIdx, False, userInfo, None, reqDate, address, hospitalLoc, reason)
    DB_addMatching(matching)
    user.addMyRequest(matchingIdx)
    DB_updateUser(user)


# 매칭 수정(병원동행) :: 요청날짜, 주소, 병원주소, 동행이유
def modifyAccompany(matchingIdx: int, reqDate: str, address: Address, hospitalLoc: Address, reason: str):
    matching = getMatching(matchingIdx)
    matching.update(reqDate, address, hospitalLoc, reason)
    DB_updateMatching(matching)


# 새로운 매칭(심리상담) 생성 :: 헬피ID, 요청날짜, 주소, 상담유형
def createCounsel(helpeeID: str, reqDate: str, address: Address, category: str):
    user = DB_getUser(helpeeID)
    userInfo = user.getUserInfo()
    matchingIdx = getMatchingNumber()

    matching = Counsel(matchingIdx, False, userInfo, None, reqDate, address, category)
    DB_addMatching(matching)
    user.addMyRequest(matchingIdx)
    DB_updateUser(user)


# 매칭 수정(심리상담) :: 요청날짜, 주소, 유형
def modifyCounsel(matchingIdx: int, reqDate: str, address: Address, category: str):
    matching = getMatching(matchingIdx)
    matching.update(reqDate, address, category)
    DB_updateMatching(matching)


# 새로운 매칭(안전점검) 생성 :: 헬피ID, 요청날짜, 주소, 점검부분
def createSafetyCheck(helpeeID: str, reqDate: str, address: Address, checkPart: str):
    user = DB_getUser(helpeeID)
    userInfo = user.getUserInfo()
    matchingIdx = getMatchingNumber()

    matching = SafetyCheck(matchingIdx, False, userInfo, None, reqDate, address, checkPart)
    DB_addMatching(matching)
    user.addMyRequest(matchingIdx)
    DB_updateUser(user)


# 매칭 수정(안전점검) :: 요청날짜, 주소, 점검부분
def modifySafetyCheck(matchingIdx: int, reqDate: str, address: Address, checkPart: str):
    matching = getMatching(matchingIdx)
    matching.update(reqDate, address, checkPart)
    DB_updateMatching(matching)


# 매칭 삭제 :: 매칭 번호
def deleteMatching(matchingIdx: int):
    matching = getMatching(matchingIdx)
    DB_deleteMatching(matchingIdx)
    user = DB_getUser(matching.getHelpeeInfo().ID)
    user.deleteMyRequest(matchingIdx)
    DB_updateUser(user)


# 매칭 하기 :: 매칭 번호, 헬퍼ID
def consentMatching(matchingIdx: int, helperID: str):
    matching = getMatching(matchingIdx)
    helper = DB_getUser(helperID)
    userInfo = helper.getUserInfo()

    matching.requireMatching(userInfo)
    DB_updateMatching(matching)

    helper.addmyHelp(matchingIdx)
    DB_updateUser(helper)