class Matching:
    """Super Class"""
    matchingSuccess = False
    matchingIdx = 0

    def __init__(self, date, address):
        self.date = date
        self.address = address

    def getDate(self):
        return self.date

    def getAddress(self):
        return self.address

    def getHelperInfo(self):
        self.helperInfo = User.getUserInfo(helper)
        return helperInfo
    
    def getHelpeeInfo(self):
        self.helpeeInfo = User.getUserInfo(helpee)
        return helpeeInfo

    def getMatchingIdx(self):
        return self.matchingIdx

    #def requireMatching(self):




class Accompany(Matching):
    helptype = 1
    def __init__(self, date, address, reason, hospitalLocation):
        self.reason = reason
        self.hospitalLocation = hospitalLocation
        Matching.matchingIdx += 1
        self.matchingIdx = Matching.matchingIdx
    
    def getReason(self):
        return self.reason

    def getHospitalLocation(self):
        return self.hospitalLocation
    


class Counsel(Matching):
    helptype = 2
    def __init__(self, date, address, category):
        self.category = category
        Matching.matchingIdx += 1
        self.matchingIdx = Matching.matchingIdx
    
    def getCategory(self):
        return self.category
    
    
class SafetyCheck(Matching):
    helptype = 4
    def __init__(self, date, address, checkpart):
        self.checkpart = checkpart
        Matching.matchingIdx += 1
        self.matchingIdx = Matching.matchingIdx
    
    def getCheckPart(self):
        return self.checkpart


if __name__=="__main__":

    m = Matching("date", "address")
    print(type(m))
    print("address: " + m.getAddress() + " date: " + m.getDate())

    a = Accompany("date", "address", "aaa", "hospital address")
    print("matching idx =", Matching.getMatchingIdx(Matching))

    b = Counsel("date", "address", "aaa")
    print("matching idx =", Matching.getMatchingIdx(Matching))

    c = SafetyCheck("date", "address", "aaa")
    print("matching idx =", Matching.getMatchingIdx(Matching))

    print("a matching idx =", a.getMatchingIdx())
