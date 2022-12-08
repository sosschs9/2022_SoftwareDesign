import pymongo
from abc import *
from basic import *
from user import *

# app.py 작성시 맨 아래쪽의 Method(app.py) 부분 참고

# DB 연결
client = pymongo.MongoClient("mongodb+srv://SD:1234@cluster0.kkapwcd.mongodb.net/?retryWrites=true&w=majority")
db = client['2022SoftwareDesign']
col_post = db['Post']


##### PD Layer Class #####
class Writing(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, writerID, writeDate, contents):
        self.__writerID = writerID
        self.__writeDate = writeDate
        self.__contents = contents

    @abstractmethod
    def delete(self):
        pass

    @abstractmethod
    def modify(self):
        pass

    @abstractmethod
    def getWriteDate(self):
        pass

    @abstractmethod
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

    # 글 삭제
    def delete(self):
        deletePost(self.__postIdx)

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

    # 댓글 삭제 ** 해당 Post의 commentList에서 삭제해야함 **
    def delete(self):
        pass

    # Comment Getter
    def getCommentIdx(self):
        return self.__commentIdx

    def getWriteDate(self):
        return self.__writeDate

    def getWriterID(self):
        return self.__writerID

    def getContents(self):
        return self.__contents


##### POST DB #####
# 새로운 게시글 번호 / ret: int
def getPostNumber():
    result = col_post.find().sort('_Post__postIdx', -1).limit(1)
    for i in result:
        return i['_Post__postIdx'] + 1
    return 1


# 게시글 추가
def DB_addPost(nPost: Post):
    element = nPost.__dict__
    element['_Post__address'] = nPost.getAddress().__dict__

    commentList = []
    for i in nPost.commentList:
        commentList.append(i.__dict__)
    element['commentList'] = commentList

    col_post.insert_one(element)


# 게시글(+댓글) 불러오기 / ret: Post
def getPost(postIdx: int):
    result = col_post.find_one({'_Post__postIdx': postIdx})

    temp = result['_Post__address']
    addr = Address(temp['detailAddress'], temp['placeName'], temp['region'])

    post = Post(result['_Post__postIdx'], result['_Post__writeDate'], result['_Post__writerID'],
                result['_Post__title'], result['_Post__contents'], result['_Post__requestDate'],
                addr, result['_Post__pay'], result['_Post__contact'], [])

    for i in result['commentList']:
        post.addComment(i['_Comment__commentIdx'], i['_Comment__writeDate'], i['_Comment__writerID'],
                        i['_Comment__contents'])

    return post


# 게시글 삭제
def DB_deletePost(postIdx: int):
    col_post.delete_one({'_Post__postIdx': postIdx})


# 게시글 업데이트
def DB_updatePost(post: Post):
    DB_deletePost(post.getPostIdx())
    DB_addPost(post)


# 총 게시글 페이지 수 / ret: int
def getAllPostPageCount():
    cnt = col_post.estimated_document_count()
    if cnt % 20 != 0:
        return int(cnt / 20) + 1
    else:
        return int(cnt / 20)


# 게시글 목록 불러오기(페이지 번호별 20개) / ret:list
# list: {'postIdx':글번호, 'region':지역, 'title':제목, 'writerID':작성자ID, 'writeDate':작성일자}
def getAllPostList(pageNumber: int):
    maxIdx = pageNumber * 20
    result = col_post.find().sort('_Post__postIdx', -1).limit(maxIdx)
    ret = []
    cnt = 0
    for element in result:
        cnt += 1
        if cnt <= (pageNumber - 1) * 20:
            continue
        else:
            ret.append({'postIdx': element['_Post__postIdx'], 'title': element['_Post__title'],
                        'region': element['_Post__address']['region'],
                        'writerID': element['_Post__writerID'], 'writeDate': element['_Post__writeDate']})
    return ret

# 총 region 페이지 수 / ret: int
def getRegionPostPageCount(region:str):
    cnt = 0
    result = col_post.find({})
    for element in result:
        if element['_Post__address']['region'] == region:
            cnt += 1

    if cnt % 20 != 0:
        return int(cnt / 20) + 1
    else:
        return int(cnt / 20)


# 지역별 게시글 목록 불러오기(페이지 번호별 20개) / ret:list
# list 형태는 getAllPostList와 같음
def getRegionPostList(pageNumber: int, region: str):
    maxIdx = pageNumber * 20
    postIdx = getPostNumber() - 1

    ret = []
    postCnt = 0
    while postIdx > 0 and len(ret) < 20:
        element = col_post.find_one({'_Post__postIdx': postIdx})
        postIdx -= 1
        if element == None:
            continue

        if element['_Post__address']['region'] == region:
            postCnt += 1
            if postCnt <= (pageNumber - 1) * 20:
                continue
            else:
                ret.append({'postIdx': element['_Post__postIdx'], 'title': element['_Post__title'],
                            'region': element['_Post__address']['region'],
                            'writerID': element['_Post__writerID'], 'writeDate': element['_Post__writeDate']})

    return ret


# 해당 유저의 게시글 목록 불러오기 / ret: list
# list 형태는 getAllPostList와 같음
def getUserPostList(postNumList: list):
    ret = []
    for i in postNumList:
        element = col_post.find_one({'_Post__postIdx': i})
        ret.append({'postIdx': element['_Post__postIdx'], 'title': element['_Post__title'],
                    'region': element['_Post__address']['region'],
                    'writerID': element['_Post__writerID'], 'writeDate': element['_Post__writeDate']})
    return ret