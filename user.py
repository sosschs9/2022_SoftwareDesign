import pymongo
from basic import *

# DB 연결
client = pymongo.MongoClient("mongodb+srv://SD:1234@cluster0.kkapwcd.mongodb.net/?retryWrites=true&w=majority")
db = client['2022SoftwareDesign']
col_user = db['User']

##### PD Layer Class #####
class User:
  # 초기화: id, password, 이름, 전화번호, 성별, myPost, myReqHistory
  def __init__(self, id:str, pw:str, name:str, phoneNumber:str, gender:bool, myPost:list, myReqHistory:list):
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
    self.__myRequestHistory(self, requestIdx)


class Helper(User):
  # 초기화: id, password, 이름, 전화번호, 성별, 도우미 유형, myPost, myReqHistory, myHelpHistory
  def  __init__(self, id:str, pw:str, name:str, phoneNumber:str, gender:bool, helperType:int, myPost:list, myReqHistory:list, myHelpHistory:list):
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
    self.__myRequestHistory(self, requestIdx)


##### USER DB #####
# 회원 등록 확인 / ret: boolean
def isRegistered(userID:str):
  element = col_user.find_one({'_User__id':userID})
  ret = False
  if element == None:
      element = col_user.find_one({'_Helper__id':userID})
      if element != None:
        ret = True
  else:
      ret = True
  return ret

# 회원 등록
def DB_addUser(nUser):
  col_user.insert_one(nUser.__dict__)

# 회원 삭제
def DB_deleteUser(userID:str):
  col_user.delete_one({'_User__id':userID})
  col_user.delete_one({'_Helper__id':userID})

# 회원 찾기 / ret: User
def DB_getUser(userID:str):
  element = col_user.find_one({'_User__id':userID})
  if element == None:
    element = col_user.find_one({'_Helper__id':userID})
    user = Helper(element['_Helper__id'], element['_Helper__password'], element['_Helper__name'], 
                  element['_Helper__phoneNumber'], element['_Helper__gender'], element['_Helper__helperType'],
                  element['_Helper__myPost'], element['_Helper__myRequestHistory'], element['_Helper__myHelpHistory'])
  else:
    user = User(element['_User__id'], element['_User__password'], element['_User__name'],
                element['_User__phoneNumber'], element['_User__gender'], element['_User__myPost'], element['_User__myRequestHistory'])
  return user

# 회원 정보 수정
def DB_updateUser(user):
    DB_deleteUser(user.getID())
    DB_addUser(user)


##### Method(app.py) #####
# 회원 등록 확인 >> isRegistered(userID:str) / ret: boolean
# User 불러오기 >> getUser(userID:str) / ret: User

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
  user = col_user.find_one({'_User__id':userID})
  if user == None:
    user = col_user.find_one({'Helper_id':userID})
    helper = Helper(user['_Helper__id'], user['_Helper__password'], user['_Helper__name'],
                    user['_Helper__phoneNumber'], user['_Helper__gender'], user['_Helper__helperType'] | helperType,
                    user['_Helper__myPost'], user['_Helper__myRequestHistory'], user['_Helper__MyHelpHistory'])
  else:
    helper = Helper(user['_User__id'], user['_User__password'], user['_User__name'],
                    user['_User__phoneNumber'], user['_User__gender'], helperType,
                    user['_User__myPost'], user['_User__myRequestHistory'], [])
  DB_deleteUser(userID)
  DB_addUser(helper)

# Helper인지확인 / ret:bool
def isHelper(userID):
  user = DB_getUser(userID)
  if type(user) == Helper:
    return True
  return False