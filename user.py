

class User:
  def __init__(self, inputid, inputpw, inputname, inputphonenumber, inputgender):
    self.id = inputid
    self.password = inputpw
    self.name = inputname
    self.phoneNumber = inputphonenumber
    self.gender = inputgender
    self.myPost = []
    self.myRequestHistory = []
  
  def getUserInfo(self):
    return (self.id, self.name, self.phoneNumber, self.gender)
  def getName(self):
    return self.name
  def getPhoneNum(self):
    return self.phoneNumber
  def getGender(self):
    return self.gender
  def getID(self):
    return self.id
  def getPassword(self):
    return self.password
  
  def update(self, pw, pn):
    self.password = pw
    self.phoneNumber = pn
  def login(self, id, pw):
    
    
    return self.id
  def addMyPost(self, idx):
    self.myPost.append(idx)
    
    return self.id
  def addMyComment(self, idx):
    
    
    return self.id
  def addMyRequest(self, idx):
    self.myRequestHistory.append(idx)
    
    return self.id
  
  
class Helper(User):
  def __init__(self, inputid, inputpw, inputname, inputphonenumber, inputgender, htype):
    self.id = inputid
    self.password = inputpw
    self.name = inputname
    self.phoneNumber = inputphonenumber
    self.gender = inputgender
    self.myPost = []
    self.myRequestHistory = []
    self.myHelpHistory = []
    self.helptype = htype
    
  def getHelperType(self):
    return self.helperType
  
  def addmyHelp(self, idx):
    self.myHelpHistory.append(idx)