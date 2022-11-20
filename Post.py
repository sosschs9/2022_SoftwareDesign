from abc import *

class Writing(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, writerID, date, contents):
        self.writerID = writerID
        self.date = date
        self.contents = contents
    
#    @abstractmethod
#    def delete(self):
#        pass

    @abstractmethod
    def modify(self):
        pass

    @abstractmethod
    def getDate(self):
        pass

    @abstractmethod
    def getWriterID(self):
        pass


class Post(Writing):
    def __init__(self, writerID, date, contents, postIdx, title, location, detailAddress, pay, commentCnt):
        self.writerID = writerID
        self.date = date
        self.contents = contents
        self.postIdx = postIdx
        self.title = title
        self.location = location
        self.detailAddress = detailAddress
        self.pay = pay
        self.commentCnt = commentCnt
    
    def modify(self, title, content, location, pay):
        self.title = title
        self.content = content
        self.location = location
        self.pay = pay

#    def delete():
#        pass

    def getDate(self):
        return self.date

    def getWriterID(self):
        return self.writerID

    def getLocation(self):
        return self.location

    def getPay(self):
        return self.pay

    def getTitle(self):
        return self.title

    def getCommentCnt(self):
        return self.commentCnt

class Comment(Writing):
    def __init__(self, writerID, date, contents, commentIdx):
        self.writerID = writerID
        self.date = date
        self.contents = contents
        self.commentIdx = commentIdx

#    def delete():
#        pass

    def modify(self, contents):
        self.contents = contents
    
    def getDate(self):
        return self.date
    
    def getWriterID(self):
        return self.writerID
    
    def getComment(self):
        return self.contents
