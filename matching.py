class Matching:
    """Super Class"""
    __matchingSuccess = False
    __matchingIdx = 0

    def __init__(self, date, address):
        self.__date = date
        self.__address = address

    def getDate(self):
        return self.__date

    def getAddress(self):
        return self.__address

    def getHelperInfo(self):
        self.__matchedHelperInfo = User.getUserInfo(helper)
        return self.__matcheHelperInfo
    
    def getHelpeeInfo(self):
        self.__matchedHelpeeInfo = User.getUserInfo(helpee)
        return self.__matchedHelpeeInfo

    def getMatchingIdx(self):
        return self.__matchingIdx

    def countMatching(self):
        self.__matchingIdx = self.__matchingIdx + 1

    def requireMatching(self):
        pass

    # dm layer 정리 후 추가 예정
    #def delete():


class Accompany(Matching):
    def __init__(self, date, address, reason, hospitalLocation):
        self.__date = date
        self.__address = address
        self.__reason = reason
        self.__hospitalLocation = hospitalLocation
        
        Matching.countMatching(Matching)
        self.__matchingIdx = super().getMatchingIdx()
    
    def getDate(self):
        return self.__date

    def getAddress(self):
        return self.__address

    def getReason(self):
        return self.__reason

    def getHospitalLocation(self):
        return self.__hospitalLocation
    
    def getMatchingIdx(self):
        return self.__matchingIdx
    
    # need modify
    def requireMatching(self):
        if self.__name__ in super().getHelperType:
            super().__matchingSuccess = True


class Counsel(Matching):
    def __init__(self, date, address, category):
        self.__date = date
        self.__address = address
        self.__category = category

        Matching.countMatching(Matching)
        self.__matchingIdx = super().getMatchingIdx()
    
    def getDate(self):
        return self.__date

    def getAddress(self):
        return self.__address
    
    def getCategory(self):
        return self.__category

    def getMatchingIdx(self):
        return self.__matchingIdx

    # need modify
    def requireMatching(self):
        if self.__name__ in super().getHelperType:
            super().__matchingSuccess = True
    
class SafetyCheck(Matching):
    def __init__(self, date, address, checkpart):
        self.__date = date
        self.__address = address
        self.__checkpart = checkpart
        
        Matching.countMatching(Matching)
        self.__matchingIdx = super().getMatchingIdx()
    
    def getDate(self):
        return self.__date

    def getAddress(self):
        return self.__address
    
    def getCheckPart(self):
        return self.__checkpart

    def getMatchingIdx(self):
        return self.__matchingIdx

    # need modify
    def requireMatching(self):
        if self.__name__ in super().getHelperType:
            super().__matchingSuccess = True

'''
if __name__=="__main__":

    m = Matching("date", "address")
    print(type(m))
    print("address: " + m.getAddress() + " date: " + m.getDate())

    a = Accompany("date", "address", "aaa", "hospital address")
    print("now matching idx =", Matching.getMatchingIdx(Matching))
    print("address: " + a.getAddress() + " date: " + a.getDate())

    b = Counsel("date", "address", "aaa")
    print("now matching idx =", Matching.getMatchingIdx(Matching))

    c = SafetyCheck("date", "address", "aaa")
    print("now matching idx =", Matching.getMatchingIdx(Matching))

    d = Accompany("date", "address", "aaa", "hospital address")
    print("now matching idx =", Matching.getMatchingIdx(Matching))

    print("a matching idx =", a.getMatchingIdx())
    print("b matching idx =", b.getMatchingIdx())
    print("c matching idx =", c.getMatchingIdx())
    print("d matching idx =", d.getMatchingIdx())

    print(type(a).__name__ == 'Accompany')
'''