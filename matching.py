import pymongo
from basic import *
from user import *
from messageSender import *

# app.py 작성시 맨 아래쪽의 Method(app.py) 부분 참고
# messageSender 부분 수정 필요(requireMatching)

# DB 연결
client = pymongo.MongoClient("mongodb+srv://SD:1234@cluster0.kkapwcd.mongodb.net/?retryWrites=true&w=majority")
db = client['2022SoftwareDesign']
col_match = db['Matching']

##### PD Layer Class #####
class Matching:
    # Super Class
    def __init__(self, matchingIdx:int, success:bool, helpee:UserCommonInfo, helper:UserCommonInfo, reqDate:str, address:Address):
        self.__matchingIdx = matchingIdx
        self.__requestDate = reqDate
        self.__address = address
        
        self.__matchingSuccess = success
        self.__matchedHelpeeInfo = helpee
        self.__matchedHelperInfo = helper

    def requireMatching(self):
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
    def __init__(self, matchingIdx:int, success:bool, helpee:UserCommonInfo, helper:UserCommonInfo, reqDate:str, address:Address, hospitalLocation:Address, reason:str):
        self.__matchingIdx = matchingIdx
        self.__requestDate = reqDate
        self.__address = address
        self.__hospitalLocation = hospitalLocation
        self.__reason = reason

        self.__matchingSuccess = success
        self.__matchedHelpeeInfo = helpee
        self.__matchedHelperInfo = helper

    def requireMatching(self, helper:UserCommonInfo):
        self.__matchingSuccess = True
        self.__matchedHelperInfo = helper
        # MessageSender.sendMatching(self, self.__matchedHelperInfo, self.__matchedHelpeeInfo, "병원 동행")

    def update(self, reqDate:str, address:Address, hospitalLoc:Address, reason:str):
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
    def __init__(self, matchingIdx:int, success:bool, helpee:UserCommonInfo, helper:UserCommonInfo, reqDate:str, address:Address, category:str):
        self.__matchingIdx = matchingIdx
        self.__requestDate = reqDate
        self.__address = address
        self.__category = category

        self.__matchingSuccess = success
        self.__matchedHelpeeInfo = helpee
        self.__matchedHelperInfo = helper

    def requireMatching(self, helper:UserCommonInfo):
        self.__matchingSuccess = True
        self.__matchedHelperInfo = helper
        # MessageSender.sendMatching(self, helper.getUserInfo(), helpee.getUserInfo(), "심리 상담")
        # MessageSender.sendAppointment(self, helper.getUserInfo(), helpee.getUserInfo(), "심리 상담")

    def update(self, reqDate:str, address:Address, category:str):
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
    def __init__(self, matchingIdx:int, success:bool, helpee:UserCommonInfo, helper:UserCommonInfo, reqDate:str, address:Address, checkPart:str):
        self.__matchingIdx = matchingIdx
        self.__requestDate = reqDate
        self.__address = address
        self.__checkPart = checkPart
        
        self.__matchingSuccess = success
        self.__matchedHelpeeInfo = helpee
        self.__matchedHelperInfo = helper

    def requireMatching(self, helper:UserCommonInfo):
        self.__matchingSuccess = True
        self.__matchedHelperInfo = helper
        # MessageSender.sendMatching(self, helper.getUserInfo(), helpee.getUserInfo(), "안전 점검")
        # MessageSender.sendAppointment(self, helper.getUserInfo(), helpee.getUserInfo(), "안전 점검")

    def update(self, reqDate:str, address:Address, checkPart:str):
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


##### Matching DB #####
# 새로운 매칭 번호 / ret: int
def getMatchingNumber():
    result = col_match.find().sort('matchingIdx', -1).limit(1)
    for i in result:
        return i['matchingIdx']+1
    return 1

# 매칭 추가
def DB_addMatching(matching):
    element = matching.__dict__
    if type(matching) == Accompany:
        element['matchingIdx'] = element['_Accompany__matchingIdx']
        element['_Accompany__address'] = matching.getAddress().__dict__
        element['_Accompany__matchedHelpeeInfo'] = matching.getHelpeeInfo().__dict__
        if element['_Accompany__matchedHelperInfo'] != None:
            element['_Accompany__matchedHelperInfo'] = matching.getHelperInfo().__dict__

        element['_Accompany__hospitalLocation'] = matching.getHospitalLocation().__dict__

    elif type(matching) == Counsel:
        element['matchingIdx'] = element['_Counsel__matchingIdx']
        element['_Counsel__address'] = matching.getAddress().__dict__
        element['_Counsel__matchedHelpeeInfo'] = matching.getHelpeeInfo().__dict__
        if element['_Counsel__matchedHelperInfo'] != None:
            element['_Counsel__matchedHelperInfo'] = matching.getHelperInfo().__dict__
    else:
        element['matchingIdx'] = element['_SafetyCheck__matchingIdx']
        element['_SafetyCheck__address'] = matching.getAddress().__dict__
        element['_SafetyCheck__matchedHelpeeInfo'] = matching.getHelpeeInfo().__dict__
        if element['_SafetyCheck__matchedHelperInfo'] != None:
            element['_SafetyCheck__matchedHelperInfo'] = matching.getHelperInfo().__dict__

    col_match.insert_one(element)

#  매칭 삭제
def DB_deleteMatching(matchingIdx:int):
    col_match.delete_one({'matchingIdx':matchingIdx})

# 매칭 불러오기 / ret: Matching(Accompany or Cousel or SafetyCheck)
def getMatching(matchingIdx:int):
    result = col_match.find_one({'_Accompany__matchingIdx':matchingIdx})
    if result != None:
        helpee = data_to_UserInfo(result, '_Accompany__matchedHelpeeInfo')
        if result['_Accompany__matchedHelperInfo'] == None:
            helper = None
        else:
            helper = data_to_UserInfo(result, '_Accompany__matchedHelperInfo')

        addr = data_to_Address(result, '_Accompany__address')
        hospitalAddr = data_to_Address(result, '_Accompany_hospitalLocation')

        matching = Accompany(result['_Accompany__matchingIdx'], result['_Accompany__matchingSuccess'], helpee, helper,
                            result['_Accompany__requestDate'], addr, hospitalAddr, result['_Accompany__reason'])
    else:
        result = col_match.find_one({'_Counsel__matchingIdx':matchingIdx})
        if result != None:
            helpee = data_to_UserInfo(result, '_Counsel__matchedHelpeeInfo')
            if result['_Counsel__matchedHelperInfo'] == None:
                helper = None
            else:
                helper = data_to_UserInfo(result, '_Counsel__matchedHelperInfo')

            addr = data_to_Address(result, '_Counsel__address')

            matching = Counsel(result['_Counsel__matchingIdx'], result['_Counsel__matchingSuccess'], helpee, helper,
                                result['_Counsel__requestDate'], addr, result['_Counsel__category'])

        else:
            result = col_match.find_one({'_SafetyCheck__matchingIdx':matchingIdx})
            helpee = data_to_UserInfo(result, '_SafetyCheck__matchedHelpeeInfo')
            if result['_SafetyCheck__matchedHelperInfo'] == None:
                helper = None
            else:
                helper = data_to_UserInfo(result, '_SafetyCheck__matchedHelperInfo')

            addr = data_to_Address(result, '_SafetyCheck__address')

            matching = SafetyCheck(result['_SafetyCheck__matchingIdx'], result['_SafetyCheck__matchingSuccess'], helpee, helper,
                                result['_SafetyCheck__requestDate'], addr, result['_SafetyCheck__checkPart'])

    return matching

# 매칭 업데이트
def DB_updateMatching(matching):
    DB_deleteMatching(matching.getMatchingIdx())
    DB_addMatching(matching)

# 총 매칭 수 / ret: int
def getAllPostPageCount(helpType:int):
    result = col_match.find({})
    cnt = 0
    
    for element in result:
        if ('_Accompany__matchingIdx' in element) and (helpType & HelperType.ACCOMPANY):
            if element['_Accompany__matchingSuccess'] == False:
                cnt += 1
        elif ('_Counsel__matchingIdx' in element) and (helpType & HelperType.COUNSEL):
            if element['_Counsel__matchingSuccess'] == False:
                cnt += 1
        elif ('_SafetyCheck__matchingIdx' in element) and (helpType & HelperType.SAFETYCHECK):
            if element['_SafetyCheck__matchingSuccess'] == False:
                cnt += 1

    if cnt % 20 != 0:
        return int(cnt / 20) + 1
    else:
        return int(cnt / 20)

# 매칭 목록 불러오기(페이지 번호별 20개) / ret: list
# list: {'matchingIdx':매칭번호, 'helpType':매칭유형, 'title':제목, 'writerID':작성자ID, 'reqDate':요청일자}
def getMatchingList(pageNumber:int, helpType:int):
    matchingIdx = getMatchingNumber()-1

    ret = []
    matchingCnt = 0
    while matchingIdx > 0 and len(ret) < 20:
        element = col_match.find_one({'matchingIdx':matchingIdx})
        matchingIdx -= 1
        if element == None:
            continue
            
        if ('_Accompany__matchingIdx' in element) and (helpType & HelperType.ACCOMPANY):
            if element['_Accompany__matchingSuccess'] == True:
                continue
            
            matchingCnt +=1
            if matchingCnt <= (pageNumber-1)*20:
                continue
            else:
                title = '['+element['_Accompany__hospitalLocation']['region']+':'+element['_Accompany__hospitalLocation']['placeName']+'] '+element['_Accompany__reason']
                if(len(title) > 30):
                    title = title[:30] + '...'
                ret.append({'matchingIdx':element['_Accompany__matchingIdx'], 'helpType':'병원동행', 
                            'title':title, 'writerID':element['_Accompany__matchedHelpeeInfo']['ID'], 'reqDate':element['_Accompany__requestDate']})

        elif ('_Counsel__matchingIdx' in element) and (helpType & HelperType.COUNSEL):
            if element['_Counsel__matchingSuccess'] == True:
                continue

            matchingCnt +=1
            if matchingCnt <= (pageNumber-1)*20:
                continue
            else:
                title = '['+element['_Counsel__address']['region']+'] '+element['_Counsel__category']
                if(len(title) > 30):
                    title = title[:30] + '...'
                ret.append({'matchingIdx':element['_Counsel__matchingIdx'], 'helpType':'심리상담', 
                            'title':title, 'writerID':element['_Counsel__matchedHelpeeInfo']['ID'], 'reqDate':element['_Counsel__requestDate']})

        elif ('_SafetyCheck__matchingIdx' in element) and (helpType & HelperType.SAFETYCHECK):
            if element['_SafetyCheck__matchingSuccess'] == True:
                continue

            matchingCnt +=1
            if matchingCnt <= (pageNumber-1)*20:
                continue
            else:
                title = '['+element['_SafetyCheck__address']['region']+'] '+element['_SafetyCheck__checkPart']
                if(len(title) > 30):
                    title = title[:30] + '...'
                ret.append({'matchingIdx':element['_SafetyCheck__matchingIdx'], 'helpType':'안전점검', 
                            'title':title, 'writerID':element['_SafetyCheck__matchedHelpeeInfo']['ID'], 'reqDate':element['_SafetyCheck__requestDate']})
    
    return ret

# 해당 유저의 매칭요청 목록 불러오기 / ret: list
# list 형태는 getMatchingList에 'status':상태(매칭완료 여부) 추가
def getUserRequestList(postNumList:list):
    ret = []
    for i in postNumList:
        element = col_match.find_one({'_Post__postIdx':i})
        if '_Accompany__matchingIdx' in element:
            title = '['+element['_Accompany__hospitalLocation']['region']+':'+element['_Accompany__hospitalLocation']['placeName']+'] '+element['_Accompany__reason']
            if(len(title) > 30):
                title = title[:30] + '...'
            ret.append({'matchingIdx':element['_Accompany__matchingIdx'], 'helpType':'병원동행', 
                        'title':title, 'writerID':element['_Accompany__matchedHelpeeInfo']['ID'],
                        'reqDate':element['_Accompany__requestDate'], 'status':element['_Accompany__matchingSuccess']})
        elif '_Counsel__matchingIdx' in element:
            title = '['+element['_Counsel__address']['region']+'] '+element['_Counsel__category']
            if(len(title) > 30):
                title = title[:30] + '...'
            ret.append({'matchingIdx':element['_Counsel__matchingIdx'], 'helpType':'심리상담', 
                        'title':title, 'writerID':element['_Counsel__matchedHelpeeInfo']['ID'], 
                        'reqDate':element['_Counsel__requestDate'], 'status':element['_Counsel__matchingSuccess']})
        elif '_SafetyCheck__matchingIdx' in element:
            title = '['+element['_SafetyCheck__address']['region']+'] '+element['_SafetyCheck__checkPart']
            if(len(title) > 30):
                title = title[:30] + '...'
            ret.append({'matchingIdx':element['_SafetyCheck__matchingIdx'], 'helpType':'안전점검', 
                        'title':title, 'writerID':element['_SafetyCheck__matchedHelpeeInfo']['ID'], 
                        'reqDate':element['_SafetyCheck__requestDate'], 'status':element['_SafetyCheck__matchingSuccess']})

    return ret

# 해당 유저(도우미)의 매칭 목록 불러오기 / ret: list
# list 형태는 getMatchingList와 같음
def getUserHelpList(postNumList:list):
    ret = []
    for i in postNumList:
        element = col_match.find_one({'_Post__postIdx':i})
        if '_Accompany__matchingIdx' in element:
            title = '['+element['_Accompany__hospitalLocation']['region']+':'+element['_Accompany__hospitalLocation']['placeName']+'] '+element['_Accompany__reason']
            if(len(title) > 30):
                title = title[:30] + '...'
            ret.append({'matchingIdx':element['_Accompany__matchingIdx'], 'helpType':'병원동행', 
                        'title':title, 'writerID':element['_Accompany__matchedHelpeeInfo']['ID'], 'reqDate':element['_Accompany__requestDate']})
        elif '_Counsel__matchingIdx' in element:
            title = '['+element['_Counsel__address']['region']+'] '+element['_Counsel__category']
            if(len(title) > 30):
                title = title[:30] + '...'
            ret.append({'matchingIdx':element['_Counsel__matchingIdx'], 'helpType':'심리상담', 
                        'title':title, 'writerID':element['_Counsel__matchedHelpeeInfo']['ID'], 'reqDate':element['_Counsel__requestDate']})
        elif '_SafetyCheck__matchingIdx' in element:
            title = '['+element['_SafetyCheck__address']['region']+'] '+element['_SafetyCheck__checkPart']
            if(len(title) > 30):
                title = title[:30] + '...'
            ret.append({'matchingIdx':element['_SafetyCheck__matchingIdx'], 'helpType':'안전점검', 
                        'title':title, 'writerID':element['_SafetyCheck__matchedHelpeeInfo']['ID'], 'reqDate':element['_SafetyCheck__requestDate']})

    return ret


##### Method(app.py) #####
# Matching 불러오기 >> getMatching(matchingIdx:int)
# 매칭 페이지 수 >> getAllPostPageCount(helpType:int)
# 매칭 목록 불러오기 >> getMatchingList(pageNumber:int, helpType:int)
# 유저 매칭요청 목록 불러오기 >> getUserRequestList(postNumList:list)
# 유저(도우미) 매칭 목록 불러오기 >> getUserHelpList(postNumList:list)

# 새로운 매칭(병원동행) 생성 :: 헬피ID, 요청날짜, 주소, 병원주소, 동행이유
def createAccompany(helpeeID:str, reqDate:str, address:Address, hospitalLoc:Address, reason:str):
    user = DB_getUser(helpeeID)
    userInfo = user.getUserInfo()
    matchingIdx = getMatchingNumber()

    matching = Accompany(matchingIdx, False, userInfo, None, reqDate, address, hospitalLoc, reason)
    DB_addMatching(matching)
    user.addMyRequest(matchingIdx)
    DB_updateUser(user)

# 매칭 수정(병원동행) :: 요청날짜, 주소, 병원주소, 동행이유
def modifyAccompany(matchingIdx:int, reqDate:str, address:Address, hospitalLoc:Address, reason:str):
    matching = getMatching(matchingIdx)
    matching.update(reqDate, address, hospitalLoc, reason)
    DB_updateMatching(matching)

# 새로운 매칭(심리상담) 생성 :: 헬피ID, 요청날짜, 주소, 상담유형
def createCounsel(helpeeID:str, reqDate:str, address:Address, category:str):
    user = DB_getUser(helpeeID)
    userInfo = user.getUserInfo()
    matchingIdx = getMatchingNumber()

    matching = Counsel(matchingIdx, False, userInfo, None, reqDate, address, category)
    DB_addMatching(matching)
    user.addMyRequest(matchingIdx)
    DB_updateUser(user)

# 매칭 수정(심리상담) :: 요청날짜, 주소, 유형
def modifyCounsel(matchingIdx:int, reqDate:str, address:Address, category:str):
    matching = getMatching(matchingIdx)
    matching.update(reqDate, address, category)
    DB_updateMatching(matching)

# 새로운 매칭(안전점검) 생성 :: 헬피ID, 요청날짜, 주소, 점검부분
def createSafetyCheck(helpeeID:str, reqDate:str, address:Address, checkPart:str):
    user = DB_getUser(helpeeID)
    userInfo = user.getUserInfo()
    matchingIdx = getMatchingNumber()

    matching = SafetyCheck(matchingIdx, False, userInfo, None, reqDate, address, checkPart)
    DB_addMatching(matching)
    user.addMyRequest(matchingIdx)
    DB_updateUser(user)

# 매칭 수정(안전점검) :: 요청날짜, 주소, 점검부분
def modifySafetyCheck(matchingIdx:int, reqDate:str, address:Address, checkPart:str):
    matching = getMatching(matchingIdx)
    matching.update(reqDate, address, checkPart)
    DB_updateMatching(matching)

# 매칭 삭제 :: 매칭 번호
def deleteMatching(matchingIdx:int):
    matching = getMatching(matchingIdx)
    DB_deleteMatching(matchingIdx)
    user = DB_getUser(matching.getHelpeeInfo().ID)
    user.deleteMyRequest(matchingIdx)
    DB_updateUser(user)

# 매칭 하기 :: 매칭 번호, 헬퍼ID
def requestMatching(matchingIdx:int, helperID:str):
    matching = getMatching(matchingIdx)
    helper = DB_getUser(helperID)
    userInfo = helper.getUserInfo()

    matching.requireMatching(userInfo)
    DB_updateMatching(matching)

    helper.addmyHelp(matchingIdx)
    DB_updateUser(helper)