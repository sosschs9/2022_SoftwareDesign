import pymongo
from basic import *

# DB 연결
client = pymongo.MongoClient("mongodb+srv://SD:1234@cluster0.kkapwcd.mongodb.net/?retryWrites=true&w=majority")
db = client['2022SoftwareDesign']
col_user = db['User']

##### PD Layer Class #####
class User:
    # 초기화: id, password, 이름, 전화번호, 성별, myPost, myReqHistory
    def __init__(self, id: str, pw: str, name: str, phoneNumber: str, gender: bool, myPost: list, myReqHistory: list):
        self.__id = id
        self.__password = pw
        self.__name = name
        self.__phoneNumber = phoneNumber
        self.__gender = gender
        self.__myPost = myPost
        self.__myRequestHistory = myReqHistory

    # 로그인 / ret:bool
    def login(self, inputID, inputPW):
        if self.getID() == inputID and self.__getPassword() == inputPW:
            return True
        else:
            return False

    def getUserInfo(self):
        return UserCommonInfo(self.__id, self.__getName(), self.__getPhoneNumber(), self.__getGender())

    # User Getter
    def getID(self):
        return self.__id

    def __getPassword(self):
        return self.__password

    def __getName(self):
        return self.__name

    def __getPhoneNumber(self):
        return self.__phoneNumber

    def __getGender(self):
        return self.__gender

    def getMyRequest(self):
        return self.__myRequestHistory

    def getMyPost(self):
        return self.__myPost

    def update(self, password, phoneNumber):
        self.__password = password
        self.__phoneNumber = phoneNumber

    def addMyPost(self, postIdx):
        self.__myPost.append(postIdx)

    def addMyRequest(self, requestIdx):
        self.__myRequestHistory.append(requestIdx)

    def deleteMyPost(self, postIdx):
        self.__myPost.remove(postIdx)

    def deleteMyRequest(self, requestIdx):
        self.__myRequestHistory.remove(requestIdx)


class Helper(User):
    # 초기화: id, password, 이름, 전화번호, 성별, 도우미 유형, myPost, myReqHistory, myHelpHistory
    def __init__(self, id: str, pw: str, name: str, phoneNumber: str, gender: bool, helperType: int, myPost: list,
                 myReqHistory: list, myHelpHistory: list):
        self.__id = id
        self.__password = pw
        self.__name = name
        self.__phoneNumber = phoneNumber
        self.__gender = gender
        self.__myPost = myPost
        self.__myRequestHistory = myReqHistory

        self.__helperType = helperType
        self.__myHelpHistory = myHelpHistory

    # 로그인 / ret:bool
    def login(self, inputID, inputPW):
        if self.getID() == inputID and self.__getPassword() == inputPW:
            return True
        else:
            return False

    def getUserInfo(self):
        return UserCommonInfo(self.__id, self.__getName(), self.__getPhoneNumber(), self.__getGender())

    # Helper Getter
    def getID(self):
        return self.__id

    def __getPassword(self):
        return self.__password

    def __getName(self):
        return self.__name

    def __getPhoneNumber(self):
        return self.__phoneNumber

    def __getGender(self):
        return self.__gender

    def getHelperType(self):
        return self.__helperType

    def getMyRequest(self):
        return self.__myRequestHistory

    def getMyPost(self):
        return self.__myPost

    def getMyHelp(self):
        return self.__myHelpHistory

    def update(self, password, phoneNumber):
        self.__password = password
        self.__phoneNumber = phoneNumber

    def addMyPost(self, postIdx):
        self.__myPost.append(postIdx)

    def addMyRequest(self, requestIdx):
        self.__myRequestHistory.append(requestIdx)

    def addmyHelp(self, helpIdx):
        self.__myHelpHistory.append(helpIdx)

    def deleteMyPost(self, postIdx):
        self.__myPost.remove(postIdx)

    def deleteMyRequest(self, requestIdx):
        self.__myRequestHistory.remove(requestIdx)

def getUser(userID: str):
    return DB_getUser(userID)

##### USER DB #####
# 회원 등록 확인 / ret: boolean
def isRegistered(userID: str):
    element = col_user.find_one({'_User__id': userID})
    ret = False
    if element == None:
        element = col_user.find_one({'_Helper__id': userID})
        if element != None:
            ret = True
    else:
        ret = True
    return ret


# 회원 등록
def DB_addUser(nUser):
    col_user.insert_one(nUser.__dict__)
    element = col_user.find_one({'_User__id':nUser.getID()})
    DB_deleteUser(nUser.getID())
    element['key'] = str(element['_id'])
    col_user.insert_one(element)

# 회원 삭제
def DB_deleteUser(userID: str):
    col_user.delete_one({'_User__id': userID})
    col_user.delete_one({'_Helper__id': userID})

# 회원 찾기 / ret: User
def DB_getUser(userID: str):
    element = col_user.find_one({'_User__id': userID})
    if element == None:
        element = col_user.find_one({'_Helper__id': userID})
        user = Helper(element['_Helper__id'], element['_Helper__password'], element['_Helper__name'],
                      element['_Helper__phoneNumber'], element['_Helper__gender'], element['_Helper__helperType'],
                      element['_Helper__myPost'], element['_Helper__myRequestHistory'],
                      element['_Helper__myHelpHistory'])
    else:
        user = User(element['_User__id'], element['_User__password'], element['_User__name'],
                    element['_User__phoneNumber'], element['_User__gender'], element['_User__myPost'],
                    element['_User__myRequestHistory'])
    return user

# key -> userID
def DB_findUser_key(userKey:str):
    element = col_user.find_one({'key':userKey})
    if element.get('_User__id') != None:
        return element['_User__id']
    else:
        return element['_Helper__id']

def DB_getUserKey(userID:str):
    element = col_user.find_one({'_User__id':userID})
    if element != None:
        return element['key']
    element = col_user.find_one({'_Helper__id':userID})
    return element['key']

# 회원 정보 수정
def DB_updateUser(user):
    element = col_user.find_one({'_User__id': user.getID()})
    if element == None:
        element = col_user.find_one({'_Helper__id': user.getID()})
    nUser = user.__dict__
    DB_deleteUser(user.getID())
    nUser['key'] = element['key']
    col_user.insert_one(nUser)