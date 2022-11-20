class Matching:
    """Super Class"""
    
    def __init__(self, date, address):
        self.date = date
        self.address = address

    def getDate(self):
        return self.date

    def getAddress(self):
        return self.address

    def getHelperInfo(self):
        return self.helperInfo
    
    def getHelpeeInfo(self):
        return self.helpeeInfo


class Accompany(Matching):
    def __init__:
        self.helptype = 1
    
    def getReason(self):
        return self.reason

    def getHospitalLocation(self):
        return self.hospitalLocation
    


class Counsel(Matching):
    def __init__:
        self.helptype = 2
    
    def getCategory(self):
        return self.category
    
    
class SafetyCheck(Matching):
    def __init__:
        self.helptype = 4
    
    def getCheckPart(self):
        return self.checkpart