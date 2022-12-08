from writing import *
from user import *

##### Method(app.py) #####
# 의뢰 게시판 페이지 수 >> getAllPostPageCount()
# 의뢰 게시판 글 목록(지역설정X) 가져오기 >> getAllPostList(pageNumber:int)
# 의뢰 게시판 글 목록(지역설정O) 가져오기 >> getRegionPostList(pageNumber:int, region:str)
# 사용자 게시판 작성 글 목록 가져오기 >> getUserPostList(postNumList:list)
# Post 불러오기(1개) >> getPost(postIdx)

# 새로운 글 생성 :: 작성자ID, 제목, 내용, 요청날짜, Address, 보수, 연락방법
def createPost(writerID: str, title: str, contents: str, reqDate: str, addr: Address, pay: str, contact: str):
    writeDate = getNowTime()
    postIdx = getPostNumber()
    nPost = Post(postIdx, writeDate, writerID, title, contents, reqDate, addr, pay, contact, [])
    DB_addPost(nPost)

    user = DB_getUser(writerID)
    user.addMyPost(postIdx)
    DB_updateUser(user)


# 글 삭제 :: 글번호
def deletePost(postIdx: int):
    post = getPost(postIdx)
    DB_deletePost(postIdx)
    user = DB_getUser(post.getWriterID())
    user.deleteMyPost(postIdx)
    DB_updateUser(user)


# 글 수정 :: 글 번호, 제목, 내용, 요청날짜, Address, 보수, 연락방법
def modifyPost(postIdx: int, title: str, contents: str, reqDate: str, addr: Address, pay: str, contact: str):
    post = getPost(postIdx)
    post.modify(title, contents, reqDate, addr, pay, contact)
    DB_updatePost(post)


# 새로운 댓글 생성:: 글번호, 작성자ID, 내용
def createComment(postIdx: int, writerID: str, contents: str):
    post = getPost(postIdx)
    commentIdx = post.getCommentCnt() + 1
    writeDate = getNowTime()
    post.addComment(commentIdx, writeDate, writerID, contents)
    DB_updatePost(post)


# 댓글 삭제:: 글번호, 댓글번호
def deleteComment(postIdx: int, commentIdx: int):
    post = getPost(postIdx)
    for comment in post.commentList:
        if comment.getCommentIdx() == commentIdx:
            index = post.commentList.index(comment)
            post.commentList.pop(index)
            DB_updatePost(post)
            return


# 댓글 수정:: 글번호, 댓글번호, 내용
def modifyComment(postIdx: int, commentIdx: int, contents: str):
    post = getPost(postIdx)
    for comment in post.commentList:
        if comment.getCommentIdx() == commentIdx:
            index = post.commentList.index(comment)
            post.commentList[index].modify(contents)
            DB_updatePost(post)
            return