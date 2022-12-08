import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from User.user import *

##### PD Layer Class #####
class Writing():
    def __init__(self, writerID, writeDate, contents):
        self.__writerID = writerID
        self.__writeDate = writeDate
        self.__contents = contents

    def delete(self):
        pass

    def modify(self):
        pass

    def getWriteDate(self):
        pass

    def getWriterID(self):
        pass


# Post Class
class Post(Writing):
    # 초기화: 글번호, 작성시간, 작성자ID, 제목, 내용, 요청날짜, 주소, 보수, 연락방법, 댓글리스트
    def __init__(self, postIdx: int, writeDate: str, writerID: str, title: str, contents: str, reqDate: str,
                 addr: Address, pay: str, contact: str, commentList: list):
        self.__postIdx = postIdx
        self.__writeDate = writeDate
        self.__writerID = writerID
        self.__title = title
        self.__contents = contents
        self.__requestDate = reqDate
        self.__address = addr
        self.__pay = pay
        self.__contact = contact
        self.commentList = commentList

    # 댓글 추가
    def addComment(self, commentIdx: int, writeDate: str, writerID: str, contents: str):
        self.commentList.append(Comment(commentIdx, writeDate, writerID, contents))

    # 글 수정
    def modify(self, title: str, contents: str, reqDate: str, addr: Address, pay: str, contact: str):
        self.__title = title
        self.__contents = contents
        self.__requestDate = reqDate
        self.__address = addr
        self.__pay = pay
        self.__contact = contact

    # Post Getter
    def getPostIdx(self):
        return self.__postIdx

    def getWriteDate(self):
        return self.__writeDate

    def getWriterID(self):
        return self.__writerID

    def getTitle(self):
        return self.__title

    def getContents(self):
        return self.__contents

    def getRequestDate(self):
        return self.__requestDate

    def getAddress(self):
        return self.__address

    def getPay(self):
        return self.__pay

    def getContact(self):
        return self.__contact

    def getCommentCnt(self):
        return len(self.commentList)


# Comment Class
class Comment(Writing):
    # 초기화: 댓글번호, 작성시간, 작성자ID, 내용
    def __init__(self, commentIdx: int, writeDate: str, writerID: str, contents: str):
        self.__commentIdx = commentIdx
        self.__writeDate = writeDate
        self.__writerID = writerID
        self.__contents = contents

    # 댓글 수정
    def modify(self, contents: str):
        self.__contents = contents

    # Comment Getter
    def getCommentIdx(self):
        return self.__commentIdx

    def getWriteDate(self):
        return self.__writeDate

    def getWriterID(self):
        return self.__writerID

    def getContents(self):
        return self.__contents