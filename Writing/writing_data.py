import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from basic import *
import pymongo
from Writing.writing import *

# DB 연결
client = pymongo.MongoClient("mongodb+srv://SD:1234@cluster0.kkapwcd.mongodb.net/?retryWrites=true&w=majority")
db = client['2022SoftwareDesign']
col_post = db['Post']

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