from basic import *
import pymongo
from Matching.matching import *

# DB 연결
client = pymongo.MongoClient("mongodb+srv://SD:1234@cluster0.kkapwcd.mongodb.net/?retryWrites=true&w=majority")
db = client['2022SoftwareDesign']
col_match = db['Matching']


##### Matching DB #####
# 새로운 매칭 번호 / ret: int
def getMatchingNumber():
    result = col_match.find().sort('matchingIdx', -1).limit(1)
    for i in result:
        return i['matchingIdx'] + 1
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
def DB_deleteMatching(matchingIdx: int):
    col_match.delete_one({'matchingIdx': matchingIdx})


# 매칭 불러오기 / ret: Matching(Accompany or Cousel or SafetyCheck)
def getMatching(matchingIdx: int):
    result = col_match.find_one({'matchingIdx': matchingIdx})
    if result.get('_Accompany__matchingIdx') != None:
        helpee = data_to_UserInfo(result, '_Accompany__matchedHelpeeInfo')
        if result['_Accompany__matchedHelperInfo'] == None:
            helper = None
        else:
            helper = data_to_UserInfo(result, '_Accompany__matchedHelperInfo')

        addr = data_to_Address(result, '_Accompany__address')
        hospitalAddr = data_to_Address(result, '_Accompany__hospitalLocation')

        matching = Accompany(result['_Accompany__matchingIdx'], result['_Accompany__matchingSuccess'], helpee, helper,
                             result['_Accompany__requestDate'], addr, hospitalAddr, result['_Accompany__reason'])
    elif result.get('_Counsel__matchingIdx') != None:
        helpee = data_to_UserInfo(result, '_Counsel__matchedHelpeeInfo')
        if result['_Counsel__matchedHelperInfo'] == None:
            helper = None
        else:
            helper = data_to_UserInfo(result, '_Counsel__matchedHelperInfo')

        addr = data_to_Address(result, '_Counsel__address')

        matching = Counsel(result['_Counsel__matchingIdx'], result['_Counsel__matchingSuccess'], helpee, helper,
                           result['_Counsel__requestDate'], addr, result['_Counsel__category'])

    else:
        print(result)
        matching = 0
        helpee = data_to_UserInfo(result, '_SafetyCheck__matchedHelpeeInfo')
        if result['_SafetyCheck__matchedHelperInfo'] == None:
            helper = None
        else:
            helper = data_to_UserInfo(result, '_SafetyCheck__matchedHelperInfo')

        addr = data_to_Address(result, '_SafetyCheck__address')

        matching = SafetyCheck(result['_SafetyCheck__matchingIdx'], result['_SafetyCheck__matchingSuccess'], helpee,
                               helper,
                               result['_SafetyCheck__requestDate'], addr, result['_SafetyCheck__checkPart'])

    return matching


# 매칭 업데이트
def DB_updateMatching(matching):
    DB_deleteMatching(matching.getMatchingIdx())
    DB_addMatching(matching)


# 총 매칭 수 / ret: int
def getAllMatchingPageCount(helpType: int):
    result = col_match.find({})
    cnt = 0

    for element in result:
        if (element.get('_Accompany__matchingIdx') != None) and (helpType & HelperType.ACCOMPANY):
            if element['_Accompany__matchingSuccess'] == False:
                cnt += 1
        elif (element.get('_Counsel__matchingIdx') != None) and (helpType & HelperType.COUNSEL):
            if element['_Counsel__matchingSuccess'] == False:
                cnt += 1
        elif (element.get('_SafetyCheck__matchingIdx') != None) and (helpType & HelperType.SAFETYCHECK):
            if element['_SafetyCheck__matchingSuccess'] == False:
                cnt += 1

    if cnt % 20 != 0:
        return int(cnt / 20) + 1
    else:
        return int(cnt / 20)


# 매칭 목록 불러오기(페이지 번호별 20개) / ret: list
# list: {'matchingIdx':매칭번호, 'helpType':매칭유형, 'title':제목, 'writerID':작성자ID, 'reqDate':요청일자}
def getMatchingList(pageNumber: int, helpType: int):
    matchingIdx = getMatchingNumber() - 1

    ret = []
    matchingCnt = 0
    while matchingIdx > 0 and len(ret) < 20:
        element = col_match.find_one({'matchingIdx': matchingIdx})
        matchingIdx -= 1
        if element == None:
            continue

        if (element.get('_Accompany__matchingIdx') != None) and (helpType & HelperType.ACCOMPANY):
            if element['_Accompany__matchingSuccess'] == True:
                continue

            matchingCnt += 1
            if matchingCnt <= (pageNumber - 1) * 20:
                continue
            else:
                title = '[' + element['_Accompany__hospitalLocation']['region'] + ':' + \
                        element['_Accompany__hospitalLocation']['placeName'] + '] ' + element['_Accompany__reason']
                if (len(title) > 30):
                    title = title[:30] + '...'
                ret.append({'matchingIdx': element['_Accompany__matchingIdx'], 'helpType': '병원동행',
                            'title': title, 'writerID': element['_Accompany__matchedHelpeeInfo']['ID'],
                            'reqDate': element['_Accompany__requestDate']})

        elif (element.get('_Counsel__matchingIdx') != None) and (helpType & HelperType.COUNSEL):
            if element['_Counsel__matchingSuccess'] == True:
                continue

            matchingCnt += 1
            if matchingCnt <= (pageNumber - 1) * 20:
                continue
            else:
                title = '[' + element['_Counsel__address']['region'] + '] ' + element['_Counsel__category']
                if (len(title) > 30):
                    title = title[:30] + '...'
                ret.append({'matchingIdx': element['_Counsel__matchingIdx'], 'helpType': '심리상담',
                            'title': title, 'writerID': element['_Counsel__matchedHelpeeInfo']['ID'],
                            'reqDate': element['_Counsel__requestDate']})

        elif (element.get('_SafetyCheck__matchingIdx') != None) and (helpType & HelperType.SAFETYCHECK):
            if element['_SafetyCheck__matchingSuccess'] == True:
                continue

            matchingCnt += 1
            if matchingCnt <= (pageNumber - 1) * 20:
                continue
            else:
                title = '[' + element['_SafetyCheck__address']['region'] + '] ' + element['_SafetyCheck__checkPart']
                if (len(title) > 30):
                    title = title[:30] + '...'
                ret.append({'matchingIdx': element['_SafetyCheck__matchingIdx'], 'helpType': '안전점검',
                            'title': title, 'writerID': element['_SafetyCheck__matchedHelpeeInfo']['ID'],
                            'reqDate': element['_SafetyCheck__requestDate']})

    return ret


# 해당 유저의 매칭요청 목록 불러오기 / ret: list
# list 형태는 getMatchingList에 'status':상태(매칭완료 여부) 추가
def getUserRequestList(postNumList: list):
    ret = []
    for i in postNumList:
        element = col_match.find_one({'_Post__postIdx': i})
        if element.get('_Accompany__matchingIdx') != None:
            title = '[' + element['_Accompany__hospitalLocation']['region'] + ':' + \
                    element['_Accompany__hospitalLocation']['placeName'] + '] ' + element['_Accompany__reason']
            if (len(title) > 30):
                title = title[:30] + '...'
            ret.append({'matchingIdx': element['_Accompany__matchingIdx'], 'helpType': '병원동행',
                        'title': title, 'writerID': element['_Accompany__matchedHelpeeInfo']['ID'],
                        'reqDate': element['_Accompany__requestDate'],
                        'status': element['_Accompany__matchingSuccess']})
        elif element.get('_Counsel__matchingIdx') != None:
            title = '[' + element['_Counsel__address']['region'] + '] ' + element['_Counsel__category']
            if (len(title) > 30):
                title = title[:30] + '...'
            ret.append({'matchingIdx': element['_Counsel__matchingIdx'], 'helpType': '심리상담',
                        'title': title, 'writerID': element['_Counsel__matchedHelpeeInfo']['ID'],
                        'reqDate': element['_Counsel__requestDate'], 'status': element['_Counsel__matchingSuccess']})
        elif element.get('_SafetyCheck__matchingIdx') != None:
            title = '[' + element['_SafetyCheck__address']['region'] + '] ' + element['_SafetyCheck__checkPart']
            if (len(title) > 30):
                title = title[:30] + '...'
            ret.append({'matchingIdx': element['_SafetyCheck__matchingIdx'], 'helpType': '안전점검',
                        'title': title, 'writerID': element['_SafetyCheck__matchedHelpeeInfo']['ID'],
                        'reqDate': element['_SafetyCheck__requestDate'],
                        'status': element['_SafetyCheck__matchingSuccess']})

    return ret


# 해당 유저(도우미)의 매칭 목록 불러오기 / ret: list
# list 형태는 getMatchingList와 같음
def getUserHelpList(postNumList: list):
    ret = []
    for i in postNumList:
        element = col_match.find_one({'_Post__postIdx': i})
        if element.get('_Accompany__matchingIdx') != None:
            title = '[' + element['_Accompany__hospitalLocation']['region'] + ':' + \
                    element['_Accompany__hospitalLocation']['placeName'] + '] ' + element['_Accompany__reason']
            if (len(title) > 30):
                title = title[:30] + '...'
            ret.append({'matchingIdx': element['_Accompany__matchingIdx'], 'helpType': '병원동행',
                        'title': title, 'writerID': element['_Accompany__matchedHelpeeInfo']['ID'],
                        'reqDate': element['_Accompany__requestDate']})
        elif element.get('_Counsel__matchingIdx') != None:
            title = '[' + element['_Counsel__address']['region'] + '] ' + element['_Counsel__category']
            if (len(title) > 30):
                title = title[:30] + '...'
            ret.append({'matchingIdx': element['_Counsel__matchingIdx'], 'helpType': '심리상담',
                        'title': title, 'writerID': element['_Counsel__matchedHelpeeInfo']['ID'],
                        'reqDate': element['_Counsel__requestDate']})
        elif element.get('_SafetyCheck__matchingIdx') != None:
            title = '[' + element['_SafetyCheck__address']['region'] + '] ' + element['_SafetyCheck__checkPart']
            if (len(title) > 30):
                title = title[:30] + '...'
            ret.append({'matchingIdx': element['_SafetyCheck__matchingIdx'], 'helpType': '안전점검',
                        'title': title, 'writerID': element['_SafetyCheck__matchedHelpeeInfo']['ID'],
                        'reqDate': element['_SafetyCheck__requestDate']})

    return ret