import requests
from flask import Flask, render_template, request, url_for, redirect, flash
from post import *
from user import *
from matching import *

app = Flask(__name__)

# Test user 불러오기
# 일반 사용자 1
# userID = "testUser"
# user = DB_getUser(userID)
# 일반 사용자 2
# userID = "testUser2"
# user = DB_getUser(userID)
# 병원동행 도우미
# userID = "helper1"
# user = DB_getUser(userID)
# 심리상담 도우미
userID = "helper2"
user = DB_getUser(userID)
# 안전점검 도우미
# userID = "helper4"
# user = DB_getUser(userID)

# checkType을 통해 matchingBoard 접근 권한 확인
isHelper = isHelper(userID)
if isHelper == False:
    checkType = 0
else:
    checkType = user.getHelperType()

# 메인페이지
@app.route('/')
def home():
    return render_template("main.html", checkType=checkType)

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

    return render_template('Post/postBoard.html', checkType=checkType,
                           page_list=page_list, max_page=max_page, this_page=page, start=block_start, end=block_end)

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
        return render_template('Post/newPost.html', checkType=checkType,)

# 의뢰 게시글 보기
@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
def view_post(post_id):
    # 게시글 불러오기
    if request.method == 'POST':
        # 댓글 작성
        comment = request.form['comment']
        createComment(post_id, userID, comment)

    post = getPost(post_id)
    return render_template('Post/readPost.html', checkType=checkType, post=post, userID=userID)

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
            return render_template("Post/modifyPost.html", checkType=checkType, post=post)

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

# 댓글 삭제하기
@app.route('/delete_comment/<int:post_id>/<int:comment_id>', methods=['GET', 'POST'])
def delete_comment(post_id, comment_id):
    post = getPost(post_id)

    deleteComment(post_id, comment_id)
    post = getPost(post_id)
    return render_template('Post/readPost.html', post=post, userID=userID)

# 도우미 매칭
@app.route('/select_helper', methods=['GET'])
def request_matching():
    return render_template('Matching/newMatching.html', checkType=checkType)

# 병원동행 도우미 신청
@app.route('/select_helper/accompany', methods=['GET', 'POST'])
def accompany_matching():
    if request.method == 'POST':
        # userinfo = user.getUserInfo()
        reqDate = request.form['date'] + " " + request.form['time']
        # 출발지 주소
        address = request.form['address']
        start_addr = Address(address, "", "")
        # 병원 주소
        address = request.form['hospital']
        hospital_addr = Address(address, "", "")
        reason = request.form['reason']

        createAccompany(userID, reqDate, start_addr, hospital_addr, reason)
        user = DB_getUser(userID)

        matchingList = user.getMyRequest()
        matchingID = matchingList[-1]

        return redirect(url_for('check_request', helpType=HelperType.ACCOMPANY, matchingID=matchingID))
    else:
        return render_template("Matching/accompanyMatching.html", checkType=checkType)

# 심리상담 도우미 요청
@app.route('/select_helper/counsel', methods=['GET', 'POST'])
def counsel_matching():
    if request.method == 'POST':
        # userinfo = user.getUserInfo()
        reqDate = request.form['date'] + " " + request.form['time']
        address = request.form['address'] + " " + request.form['detailAddress']
        addr = Address(address, "", "")
        category = request.form['category']

        createCounsel(userID, reqDate, addr, category)
        user = DB_getUser(userID)

        matchingList = user.getMyRequest()
        matchingID = matchingList[-1]

        return redirect(url_for('check_request', helpType=HelperType.COUNSEL, matchingID=matchingID))
    else:
        return render_template("Matching/counselMatching.html", checkType=checkType)

# 안전점검 도우미 요청
@app.route('/select_helper/safe', methods=['GET', 'POST'])
def safe_matching():
    if request.method == 'POST':
        # userinfo = user.getUserInfo()
        reqDate = request.form['date'] + " " + request.form['time']
        address = request.form['address'] + " " + request.form['detailAddress']
        addr = Address(address, "", "")
        category = request.form['category']

        createSafetyCheck(userID, reqDate, addr, category)
        user = DB_getUser(userID)

        matchingList = user.getMyRequest()
        matchingID = matchingList[-1]

        return redirect(url_for('check_request', helpType=HelperType.SAFETYCHECK, matchingID=matchingID))
    else:
        return render_template("Matching/safeMatching.html", checkType=checkType)

@app.route('/check_request/<int:helpType>/<int:matchingID>', methods=['GET', 'POST'])
def check_request(helpType, matchingID):
    check = {}
    if request.method == 'POST':
        # 신청 취소
        flash("매칭 신청이 완료되었습니다.")
        return redirect(url_for('home'))
    else:
        matching = getMatching(matchingID)
        check['username'] = user.getUserInfo().NAME
        # 작성자, 날짜, 장소, 상세 내용
        if type(matching) is Accompany:
            check['helpType'] = "병원동행"
            check['date'] = matching.getRequestDate()
            check['address'] = "[출발지] " + matching.getAddress().detailAddress + " [병원위치] " + matching.getHospitalLocation().detailAddress
            check['detail'] = "[동행사유] " + matching.getReason()

        elif type(matching) is Counsel:
            check['helpType'] = "심리상담"
            check['date'] = matching.getRequestDate()
            check['address'] = matching.getAddress().detailAddress
            check['detail'] = "[상담분야] " + matching.getCategory()

        elif type(matching) is SafetyCheck:
            check['helpType'] = "안전점검"
            check['date'] = matching.getRequestDate()
            check['address'] = matching.getAddress().detailAddress
            check['detail'] = "[점검부분] " + matching.getCheckPart()

        return render_template('check.html', matchingID=matchingID, check=check)

# 매칭 취소/삭제하기
@app.route('/delete_matching/<int:matchingID>')
def delete_matching(matchingID):
    deleteMatching(matchingID)
    return redirect(url_for('home'))

# 도우미 신청 목록 보기
@app.route('/matching_board/<int:helperType>/<int:page>', methods=['GET'])
def matching_board(helperType, page):
    if (helperType == 0):
        flash("도우미만 해당 페이지에 접근할 수 있습니다.", 'error')
        return redirect(url_for('home'))

    # 목록 리스트 불러오기
    page_list = getMatchingList(page, helperType)
    max_page = getAllMatchingPageCount(helperType)

    block_size = 5
    block_num = int((page - 1)/block_size)
    block_start = (block_size * block_num) + 1
    block_end = block_start + (block_size - 1)

    return render_template('Matching/matchingBoard.html', checkType=checkType,
                           page_list=page_list, max_page=max_page, this_page=page, start=block_start, end=block_end)

# 개별 매칭 보기
@app.route('/matching/<int:matching_id>', methods=['GET'])
def view_matching(matching_id):
    # 매칭 내용 불러오기
    matching = getMatching(matching_id)

    if type(matching) is Accompany:
        helpType = "병원동행 "
    elif type(matching) is Counsel:
        helpType = "심리상담 "
    elif type(matching) is SafetyCheck:
        helpType = "안전점검 "

    return render_template('Matching/readMatching.html', checkType=checkType, helpType=helpType, matching=matching)

@app.route('/consent_matching/<int:matchingID>')
def consent_matching(matchingID):
    requestMatching(matchingID, userID)
    # 메시지 전송 + 메시지 전송 예약
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.secret_key = '1234'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run()