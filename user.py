
class User:
    def __init__(self, inputid, inputpw, inputname, inputphonenumber, inputgender):
        self.__id = inputid
        self.__password = inputpw
        self.__name = inputname
        self.__phoneNumber = inputphonenumber
        self.__gender = inputgender
        self.__myPost = []
        self.__myRequestHistory = []

    def getUserInfo(self):
        return (self.__id, self.__name, self.__phoneNumber, self.__gender)
    def __getName(self):
        return self.__name
    def __getPhoneNum(self):
        return self.__phoneNumber
    def __getGender(self):
        return self.__gender
    def getID(self):
        return self.__id
    def __getPassword(self):
        return self.__password

    def update(self, pw, pn):
        self.__password = pw
        self.__phoneNumber = pn
    def login(self, id, pw):
        pass
    def addMyPost(self, idx):
        self.__myPost.append(idx)
    def addMyComment(self, idx):
        pass
    def addMyRequest(self, idx):
        self.__myRequestHistory.append(idx)


class Helper(User):
    def __init__(self, inputid, inputpw, inputname, inputphonenumber, inputgender, htype):
        self.__id = inputid
        self.__password = inputpw
        self.__name = inputname
        self.__phoneNumber = inputphonenumber
        self.__gender = inputgender
        self.__myPost = []
        self.__myRequestHistory = []
        self.__myHelpHistory = []
        self.__helpType = htype

    def getUserInfo(self):
        return (self.__id, self.__name, self.__phoneNumber, self.__gender, self.__helpType)
    def __getName(self):
        return self.__name
    def __getPhoneNum(self):
        return self.__phoneNumber
    def __getGender(self):
        return self.__gender
    def getID(self):
        return self.__id
    def __getPassword(self):
        return self.__password

    def update(self, pw, pn):
        self.__password = pw
        self.__phoneNumber = pn
    def login(self, id, pw):
        pass
    def addMyPost(self, idx):
        self.__myPost.append(idx)
    def addMyComment(self, idx):
        pass
    def addMyRequest(self, idx):
        self.__myRequestHistory.append(idx)

    def getHelperType(self):
        return self.__helpType

    def addmyHelp(self, idx):
        self.__myHelpHistory.append(idx)

'''
if __name__ == '__main__':
  u1 = Helper("abd","1234","kim","01092190120",0,1)
  u2 = User("abc","1234","lee","01012 345678",1)
  print(u1.getID(), u1.getUserInfo(), u1.getHelperType())
  print(u2.getID(), u2.getUserInfo())

  u1.addmyHelp(1)
  u1.addMyPost(2)
  u1.addMyRequest(3)

  u2.addMyPost(4)
  u2.addMyRequest(5)

  print(u1._Helper__myHelpHistory, u1._Helper__myPost, u1._Helper__myRequestHistory)
  print(u2._User__myPost, u2._User__myRequestHistory)
'''