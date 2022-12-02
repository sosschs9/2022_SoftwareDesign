import requests
from flask import Flask, render_template, request, url_for, redirect, flash
from post import *
from user import *
from matching import *
from database import findUser

app = Flask(__name__)

# default user 불러오기
userID = "testUser"
user = findUser(userID)

# 메인페이지
@app.route('/')
def home():
    return render_template("main.html")

# 의뢰 게시판 보기
@app.route('/post_board/<int:page>', methods=['GET'])
def post_board(page):
    # 게시판 리스트 불러오기
    page_list = getAllPostList(page)
    max_page = getAllPostPageCount()

    block_size = 5
    block_num = int((page - 1)/block_size)
    block_start = (block_size * block_num) + 1
    block_end = block_start + (block_size - 1)

    return render_template('Post/postBoard.html',
                           page_list=page_list, max_page=max_page, this_page = page, start=block_start, end=block_end)

# 의뢰 게시글 작성하기
@app.route('/write_post', methods=['GET', 'POST'])
def writing_post():
    if request.method == 'POST':
        writerID = userID
        title = request.form['title']
        contents = request.form['contents']
        reqDate = request.form['date']
        sido = request.form['sido']
        address = request.form['address'] + " " + request.form['detailAddress']
        addr = Address(address, "", sido)
        pay = str(request.form['pay'])
        contact = request.form['contact']

        createPost(writerID, title, contents, reqDate, addr, pay, contact)

        return redirect('/post_board/1')
    else:
        return render_template('Post/newPost.html')

# 의뢰 게시글 보기
@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
def view_post(post_id):
    # 게시글 불러오기
    if request.method == 'POST':
        # 댓글 작성
        comment = request.form['comment']
        createComment(post_id, userID, comment)

    post = getPost(post_id)
    return render_template('Post/readPost.html', post=post, userID=userID)

# 의뢰 게시글 삭제하기
@app.route('/delete_post/<int:post_id>')
def delete_post(post_id):
    post = getPost(post_id)
    if post.getWriterID() != userID:
        flash("글 삭제 권한이 없습니다.")
        return redirect('/post_board/1')
    
    deletePost(post_id)
    return redirect('/post_board/1')

# 의뢰 게시글 수정하기
@app.route('/modify_post/<int:post_id>', methods=['GET', 'POST'])
def modify_post(post_id):
    post = getPost(post_id)
    if post.getWriterID() != userID:
        flash("글 수정 권한이 없습니다.")
        return redirect('/post_board/1')
    
    if request.method == 'GET':
        if post is None:
            flash("해당 게시물이 존재하지 않습니다.")
            return redirect('/post_board/1')
        else:
            return render_template("Post/modifyPost.html", post=post)

    else:
        title = request.form['title']
        contents = request.form['contents']
        reqDate = request.form['date']
        sido = request.form['sido']
        address = request.form['address'] + " " + request.form['detailAddress']
        addr = Address(address, "", sido)
        pay = str(request.form['pay'])
        contact = request.form['contact']

        modifyPost(post_id, title, contents, reqDate, addr, pay, contact)
        return redirect('/post_board/1')

# 도우미 매칭
@app.route('/select_helper', methods=['GET'])
def request_matching():
    return render_template('Matching/newMatching.html')

# 병원동행 도우미 신청
@app.route('/select_helper/accompany', methods=['GET', 'POST'])
def accompany_matching():
    if request.method == 'POST':
        # 유저 정보 불러오기
        reqDate = request.form['date']
        time = request.form['time']
        hospital = request.form['hospital']
        reason = request.form['reason']

        #reqMatching

        return redirect(url_for('check_request', ))
    else:
        return render_template("Matching/accompanyMatching.html")

# 심리상담 도우미 요청
@app.route('/select_helper/counsel', methods=['GET', 'POST'])
def counsel_matching():
    if request.method == 'POST':
        # 유저 정보 불러오기

        return render_template('check.html')
    else:
        return render_template("Matching/counselMatching.html")

# 안전점검 도우미 요청
@app.route('/select_helper/safe', methods=['GET', 'POST'])
def safe_matching():
    if request.method == 'POST':
        # 유저 정보 불러오기

        return render_template('check.html')
    else:
        return render_template("Matching/safeMatching.html")

# @app.route('/select_helper/check_request/<str:param_userID>',  methods=['GET', 'POST'])
# def check_request(param_userID):
#     if request.method == 'POST':
#         # DB 저장
#         return render_template('')
#     else:
#         check_data = {}
#         return render_template('check.html', userID=param_userID, check_data=check_data)

# 도우미 신청 목록 보기
@app.route('/matching_board/<int:page>', methods=['GET'])
def matching_board(page):
    # 목록 리스트 불러오기
    return render_template('Matching/matchingBoard.html')

# 개별 매칭 보기
@app.route('/matching/<int:matching_id>', methods=['GET'])
def view_matching(matching_id):
    # 매칭 내용 불러오기
    return render_template('Matching/readMatching.html')


if __name__ == '__main__':
    app.run()
