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
    helptype = 1
    def __init__(self, reason, hospitalLocation):
        self.reason = reason
        self.hospitalLocation = hospitalLocation
    
    def getReason(self):
        return self.reason

    def getHospitalLocation(self):
        return self.hospitalLocation
    


class Counsel(Matching):
    helptype = 2
    def __init__(self):
        self.category = category
    
    def getCategory(self):
        return self.category
    
    
class SafetyCheck(Matching):
    helptype = 4
    def __init__(self, checkpart):
        self.checkpart = checkpart
    
    def getCheckPart(self):
        return self.checkpart