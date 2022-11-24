from abc import *

"""abstract class"""
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
#    __commentCnt = 0
    """ commentIdx : 댓글 번호"""
    __commentIdx = 0
    commentList = []

    def __init__(self, writerID, date, contents, postIdx, title, location, detailAddress, pay):
        self.__writerID = writerID
        self.__date = date
        self.__contents = contents
        self.__postIdx = postIdx
        self.__title = title
        self.__location = location
        self.__detailAddress = detailAddress
        self.__pay = pay
    

    """ Post안에 Comment가 있으므로 """
    class Comment(Writing):
        def __init__(self, writerID, date, contents, commentIdx):
            self.__writerID = writerID
            self.__date = date
            self.__contents = contents
            self.__commentIdx = commentIdx

    #    def delete():
    #        pass

        def modify(self, contents):
            self.__contents = contents
        
        def getDate(self):
            return self.__date
        
        def getWriterID(self):
            return self.__writerID
        
        def getComment(self):
            return self.__contents

    def createComment(self, commentWriterID, commentDate, commentContents):
        self.__commentIdx += 1
        globals()['comment_{0}'.format(self.__commentIdx)] = Post.Comment(commentWriterID, commentDate, commentContents, self.__commentIdx)
        self.commentList.append(globals()['comment_{0}'.format(self.__commentIdx)])

    def modify(self, title, content, location, pay):
        self.__title = title
        self.__content = content
        self.__location = location
        self.__pay = pay

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

"""    
A = Post(1, "20221124", "aaa", 2, "title", "location", "address", 10000)
A.createComment(10, "20221125", "bbbbb")
A.createComment(20, "20221126", "ccccc")
A.createComment(30, "20221127", "ddddd")
print(A.getCommentCnt())
print(globals()['comment_{}'.format(1)])
A.commentList.remove(globals()['comment_{}'.format(1)])
print(A.commentList[0].getDate())
print(A.commentList[1].getWriterID())
"""
