import pymongo
from user import *
from matching import *
from post import *
from basic import *

# DB 연결
client = pymongo.MongoClient("mongodb+srv://SD:1234@cluster0.kkapwcd.mongodb.net/?retryWrites=true&w=majority")
db = client['2022SoftwareDesign']
col_user = db['User']
col_post = db['Post']
col_match = db['Matching']


# USER DB
# 회원 등록 확인 / ret: boolean
def isRegistered(userID: str):
    result = col_user.find_one({'_User__id': userID})
    if result == None:
        return False
    else:
        return True


# 회원 등록
def addUser(nUser: User):
    col_user.insert_one(nUser.__dict__)


# 회원 삭제
def deleteUser(userID: str):
    col_user.delete_one({'_User__id': userID})


# 회원 찾기 / ret: dictionary
def findUser(userID: str):
    return col_user.find_one({'_User__id': userID})


# 회원 정보 수정 / my~ 추가
def updateUser(nUser: User):
    element = findUser(nUser.getID())
    new_element = nUser.__dict__.copy()
    new_element['_id'] = element['_id']  # '_id': DB내 식별번호
    deleteUser(nUser.getID())
    col_user.insert_one(new_element)


# POST DB
# 새로운 게시글 번호 / ret: int
def getPostNumber():
    result = col_post.find().sort('_Post__postIdx', -1).limit(1)
    for i in result:
        return i['_Post__postIdx'] + 1
    return 1


# 게시글 추가
def addPost(nPost: Post):
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

    post = Post(result['_Post__writerID'], result['_Post__date'], result['_Post__contents'], result['_Post__postIdx'],
                result['_Post__title'], addr, result['_Post__pay'])

    for i in result['commentList']:
        post.createComment(i['_Comment__writerID'], i['_Comment__date'], i['_Comment__contents'],
                           i['_Comment__commentIdx'])

    return post


# 게시글 삭제
def deletePost(postNumber: int):
    col_post.delete_one({'_Post__postNumber': postNumber})


# 게시글 수정
def updateMatching(post: Post):
    element = getPost(post.getPostIdx())
    new_element = post.__dict__.copy()
    new_element['_id'] = element['_id']  # '_id': DB내 식별번호
    deletePost(post.getPostIdx())
    col_post.insert_one(new_element)


# 게시글 목록 불러오기(20개) / ret: list
def getAllPostList(pageNumber: int):
    maxIdx = pageNumber * 20
    result = col_post.find().sort('_Post__postIdx', -1).limit(maxIdx)
    ret = []
    cnt = 0
    for i in result:
        cnt += 1
        if cnt <= (pageNumber - 1) * 20:
            continue
        else:
            ret.append(i)
    return ret


# 해당 유저의 게시글 목록 불러오기 / ret: list
def getUserPostList(postNumList: list):
    ret = []
    for i in postNumList:
        ret.append(col_post.find_one({'_Post__postIdx': i}))
    return ret


# Matching
# 매칭 요청 추가
def addMatching(nMatching: Matching):
    col_match.insert_one(nMatching.__dict__)


# 매칭 요청 찾기 / ret: Matching(Accompany/Counsel/SafetyCheck)
def getMatching(matchingIdx: int):
    result = col_match.find_one({'_Accompany__matchingIdx': matchingIdx})
    if result != None:
        return Accompany(result['_Accompany__date'], result['_Accompany__address'], result['_Accompany__reason'],
                         result['_Accompany__hospitalLocation'])
    result = col_match.find_one({'_Counsel__matchingIdx': matchingIdx})
    if result != None:
        return Counsel(result['_Counsel__date'], result['_Counsel__address'], result['_Counsel__category'])
    result = col_match.find_one({'_SafetyCheck__matchingIdx': matchingIdx})
    if result != None:
        return SafetyCheck(result['_SafetyCheck__date'], result['_SafetyCheck__address'],
                           result['_SafetyCheck__checkpart'])
    return None


# 매칭 Idx 번호 / ret: int
def getMatchNumber():
    result = col_match.find().sort().limit(1)
    for i in result:
        return i['Accompany__matchingIdx'] + 1
    return 0


# 매칭 요청 목록 불러오기(20개) / ret: list
def getMatchingList_All(pageNumber: int):
    maxIdx = pageNumber * 20
    result = col_match.find().sort('_Matching__matchingIdx', -1).limit(maxIdx)
    ret = []
    cnt = 0
    for i in result:
        cnt += 1
        if cnt <= (pageNumber - 1) * 20:
            continue
        else:
            ret.append(i)
    return ret


def getMatchingList_Type(pageNumber: int, matchType: int):
    maxIdx = pageNumber * 20
    result = col_match.find().sort('_Matching__matchingIdx', -1)
    ret = []
    cnt = 0
    for i in result:

        cnt += 1
        if cnt > maxIdx:
            break
        if cnt <= (pageNumber - 1) * 20:
            continue
        else:
            ret.append(i)
    return ret


# 매칭 내용 업데이트(수정/취소/성공)
def updateMatching(matching: Matching):
    element = getMatching(matching.getMatchingIdx())
    new_element = matching.__dict__.copy()
    new_element['_id'] = element['_id']  # '_id': DB내 식별번호
    matchType = ''
    if element['_Accompany__matchingIdx'] != None:
        matchType = '_Accompany__matchingIdx'
    elif element['_Counsel__matchingIdx'] != None:
        matchType = '_Counsel__matchingIdx'
    else:
        matchType = '_Counsel__matchingIdx'

    col_match.delete_one({matchType: element[matchType]})
    col_post.insert_one(new_element)


# test용 main
if __name__ == '__main__':
    # deleteUser('testUser')
    addr = Address("상세주소", '건물명', '지역')
    nUser = User('testUser2', '1234', '테스트2', '010-1234-5678', True)
    help = Helper('testHelper', '5678', '헬퍼', '010-0000-0000', True, 1)
    nMatch = Accompany('20221126', '주소', '이유', '병원위치')
    nPost = Post(1, "20221124", "aaa", 2, "title", addr, 10000)

    # col_post.delete_many({})
    # A = Post(1, "20221124", "aaa", 2, "title", addr, 10000)
    # A.createComment(10, "20221125", "bbbbb", 1)
    # A.createComment(20, "20221126", "ccccc", 2)
    # A.createComment(30, "20221127", "ddddd", 3)
    # addPost(A)

    # result = getPost(2)

    # print(getPostNumber())
    # col_post.delete_many({})
    # # nMatch.getMatchingIdx()
    # addMatching(nMatch)
    # addMatching(nMatch)

    # col_post.delete_many({})
    # for i in range(1, 51):
    #     nPost = Post('testUser', '20221126', '내용', i, '제목', '위치', '상세주소', '금액')
    #     addPost(nPost)
    # print(getPostNumber())

    # ret = getAllPostList(4)
    # for i in ret:
    #     print(i)

    # print(len(ret))
    # addUser(user)
    # modifyUser(nUser)
    # addUser(nUser)
    # print(nUser.getUserInfo())
    # user = findUser('testUser')
    # print(user.id)
    # print(isRegistered("testUser"))