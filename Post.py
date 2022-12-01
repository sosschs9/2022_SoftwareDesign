from abc import *

# """abstract class"""
class Writing(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, writerID, date, contents):
        self.__writerID = writerID
        self.__date = date
        self.__contents = contents
    
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
    def __init__(self, writerID:str, date, contents:str, postIdx:int, title:str, addr:Address, pay:str):
        self.__writerID = writerID
        self.__date = date
        self.__contents = contents
        self.__postIdx = postIdx
        self.__title = title
        self.__address = addr
        self.__pay = pay
        self.commentList = []
    

    # """ Post안에 Comment가 있으므로 """
    class Comment(Writing):
        def __init__(self, writerID:str, date, contents:str, commentIdx:int):
            self.__writerID = writerID
            self.__date = date
            self.__contents = contents
            self.__commentIdx = commentIdx

    # """ DM Layer 후에 완성"""
    #    def delete():
    #        pass

        def modify(self, contents):
            self.__contents = contents
        
        def getDate(self):
            return self.__date
        
        def getWriterID(self):
            return self.__writerID
        
        def getContents(self):
            return self.__contents
        
        def getCommentIdx(self):
            return self.__commentIdx

    def createComment(self, commentWriterID:str, commentDate, commentContents:str, commentIdx:int):
        self.commentList.append(Post.Comment(commentWriterID, commentDate, commentContents, commentIdx))

    def modify(self, title, content, location, pay):
        self.__title = title
        self.__content = content
        self.__location = location
        self.__pay = pay

    # """ DM Layer 후에 완성"""
#    def delete():
#        pass

    def getDate(self):
        return self.__date

    def getWriterID(self):
        return self.__writerID

    def getLocation(self):
        return self.__location

    def getPay(self):
        return self.__pay

    def getTitle(self):
        return self.__title

    def getCommentCnt(self):
        return len(self.commentList)