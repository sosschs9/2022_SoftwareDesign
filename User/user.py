import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import pymongo
from basic import *

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