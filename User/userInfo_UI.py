import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from User.user import *
from User.user_data import *
from basic import *

##### Method(app.py) #####
# 회원 등록 확인 >> isRegistered(userID:str) / ret: boolean
# User 불러오기 >> DB_getUser(userID:str) / ret: User

# 로그인 :: id, password
# 성공시 ret: bool(True), str(userID)
# 실패시 ret: bool(False), str(errorMsg)
def login(inputID, inputPW):
    if isRegistered(inputID) == False:
        return False, "등록되지 않은 회원입니다."

    user = DB_getUser(inputID)
    if user.login(inputID, inputPW) == True:
        return True, inputID
    else:
        return False, "아이디, 비밀번호가 일치하지 않습니다."


# 회원 등록 :: id, password, name, gender
def createUser(userID, password, name, phoneNumber, gender):
    user = User(userID, password, name, phoneNumber, gender, [], [])
    DB_addUser(user)

# 회원정보 수정
def modifyUser(userID, password, phoneNumber):
    user = DB_getUser(userID)
    user.update(password, phoneNumber)
    DB_updateUser(user)


# 도우미 변환
def beHelper(userID, helperType):
    user = col_user.find_one({'_User__id': userID})
    if user == None:
        user = col_user.find_one({'Helper_id': userID})
        helper = Helper(user['_Helper__id'], user['_Helper__password'], user['_Helper__name'],
                        user['_Helper__phoneNumber'], user['_Helper__gender'], user['_Helper__helperType'] | helperType,
                        user['_Helper__myPost'], user['_Helper__myRequestHistory'], user['_Helper__MyHelpHistory'])
    else:
        helper = Helper(user['_User__id'], user['_User__password'], user['_User__name'],
                        user['_User__phoneNumber'], user['_User__gender'], helperType,
                        user['_User__myPost'], user['_User__myRequestHistory'], [])
    DB_updateUser(helper)


# Helper인지확인 / ret:bool
def isHelper(userID):
    user = DB_getUser(userID)
    if type(user) == Helper:
        return True
    return False