import requests, sys, os, socket
from flask import Flask, render_template, request, url_for, redirect, flash, g
from post import *
from user import *
from matching import *


class curUser:
    isLogin = False
    userID = None
    user = None
    isHelper = False
    checkType = 0
    userKey = None


# 로컬 실행경로
# 로컬에서 실행 후 '기본주소/dev'로 접속하기 (http://127.0.0.1:5000/dev)
path = '/dev'

app = Flask(__name__, static_url_path='/dev')


# 메인페이지
@app.route(path + '/')
def home():
    curUser.userKey = None
    curUser.userID = None
    curUser.isHelper = False
    curUser.checkType = 0
    curUser.isLogin = False
    return render_template("main.html", checkType=curUser.checkType, isLogin=curUser.isLogin)


@app.route(path + '/<userKey>')
def home_userID(userKey):
    curUser.userKey = userKey
    curUser.isLogin = True
    curUser.userID = DB_findUser_key(userKey)
    curUser.user = DB_getUser(curUser.userID)
    if type(curUser.user) == Helper:
        curUser.checkType = curUser.user.getHelperType()
        curUser.isHelper = True

    if curUser.userID == None:
        return redirect('/logout')

    return render_template("main.html", checkType=curUser.checkType, isLogin=curUser.isLogin, userKey=userKey)


# 로그인
@app.route(path + '/login_page', methods=['GET', 'POST'])
def login_page():
    if request.method == 'GET':
        return render_template("login.html")

    if request.method == 'POST':
        inputID = request.form.get('userID')
        inputPW = request.form.get('userPW')

        success, result = login(inputID, inputPW)
        if success == False:
            # flash(result)
            return render_template("login.html", checkType=curUser.checkType, message=result, isLogin=curUser.isLogin)
        else:
            curUser.userID = result
            userKey = DB_getUserKey(curUser.userID)

            return redirect('/dev/' + userKey)
    else:
        return render_template("login.html", checkType=curUser.checkType, message="", isLogin=curUser.isLogin)


# 로그out
@app.route(path + '/logout')
def logout():
    curUser.isLogin = False
    curUser.userID = None
    curUser.user = None
    curUser.isLogin = False
    curUser.checkType = 0
    return redirect('/dev')


# 의뢰 게시판 보기
@app.route(path + '/post_board/<int:page>/', methods=['GET'])
def post_board_logout(page):
    return redirect('/dev/login_page')


@app.route(path + '/post_board/<int:page>/<userKey>', methods=['GET', 'POST'])
def post_board_userKey(page, userKey):
    curUser.userKey = userKey
    curUser.isLogin = True
    curUser.userID = DB_findUser_key(userKey)
    curUser.user = DB_getUser(curUser.userID)
    if isHelper(curUser.userID):
        curUser.isHelper = True
        curUser.checkType = curUser.user.getHelperType()

    if curUser.userID == None:
        return redirect('/dev/login_page')

    if request.method == 'POST':
        category = request.form['demo-category']
        return redirect('/dev/post_board/' + category + '/' + '/' + str(page))

    return redirect('/dev/post_board/전체/' + str(page))


@app.route(path + '/post_board/<int:page>', methods=['GET', 'POST'])
def post_board(page):
    if curUser.userID == None:
        return redirect('/dev/login_page')
    # 게시판 리스트 불러오기
    page_list = getAllPostList(page)
    max_page = getAllPostPageCount()

    block_size = 5
    block_num = int((page - 1) / block_size)
    block_start = (block_size * block_num) + 1
    block_end = block_start + (block_size - 1)

    return render_template('Post/postBoard.html', checkType=curUser.checkType,
                           page_list=page_list, max_page=max_page, this_page=page, start=block_start,
                           end=block_end, isLogin=curUser.isLogin, userKey=curUser.userKey)


@app.route(path + '/post_board/<region>/<int:page>', methods=['GET', 'POST'])
def post_board_region(region, page):
    if curUser.userID == None:
        return redirect('/dev/login_page')

    if region == '전체':
        page_list = getAllPostList(page)
        max_page = getAllPostPageCount()
    else:
        # 게시판 리스트 불러오기
        page_list = getRegionPostList(page, region)
        max_page = getRegionPostPageCount(region)

    block_size = 5
    block_num = int((page - 1) / block_size)
    block_start = (block_size * block_num) + 1
    block_end = block_start + (block_size - 1)

    return render_template('Post/postBoard.html', checkType=curUser.checkType,
                           page_list=page_list, max_page=max_page, this_page=page, start=block_start,
                           end=block_end, isLogin=curUser.isLogin, userKey=curUser.userKey, region=region)


# 의뢰 게시글 작성하기
@app.route(path + '/write_post/<userKey>', methods=['GET', 'POST'])
def writing_post(userKey):
    curUser.userKey = userKey
    curUser.isLogin = True
    curUser.userID = DB_findUser_key(userKey)
    curUser.user = DB_getUser(curUser.userID)
    if isHelper(curUser.userID):
        curUser.isHelper = True
        curUser.checkType = curUser.user.getHelperType()

    if curUser.userID == None:
        return redirect('/dev/login_page')

    if request.method == 'POST':
        writerID = curUser.userID
        title = request.form['title']
        contents = request.form['contents']
        reqDate = request.form['date']
        sido = request.form['sido']
        address = request.form['address'] + " " + request.form['detailAddress']
        addr = Address(address, "", sido)
        pay = str(request.form['pay'])
        contact = request.form['contact']

        createPost(writerID, title, contents, reqDate, addr, pay, contact)

        return redirect(url_for('post_board', page=1))
    else:
        return render_template('Post/newPost.html', checkType=curUser.checkType, isLogin=curUser.isLogin,
                               userKey=curUser.userKey)


# 의뢰 게시글 보기
@app.route(path + '/post/<int:post_id>/<userKey>', methods=['GET', 'POST'])
def view_post_key(post_id, userKey):
    curUser.userKey = userKey
    curUser.isLogin = True
    curUser.userID = DB_findUser_key(userKey)
    curUser.user = DB_getUser(curUser.userID)
    if isHelper(curUser.userID):
        curUser.isHelper = True
        curUser.checkType = curUser.user.getHelperType()

    if curUser.userID == None:
        return redirect('/dev/login_page')

    if request.method == 'POST':
        # 댓글 작성
        comment = request.form['comment']
        createComment(post_id, curUser.userID, comment)

    return redirect(url_for('view_post', post_id=post_id))


@app.route(path + '/post/<int:post_id>/', methods=['GET', 'POST'])
def view_post(post_id):
    if curUser.userID == None:
        return redirect('/dev/login_page')
    # 게시글 불러오기
    post = getPost(post_id)
    result = getPost(post_id).__dict__
    result['_Post__address'] = post.getAddress().__dict__
    result['commentList'] = []
    for element in post.commentList:
        print(element)
        result['commentList'].append(element.__dict__)

    return render_template('Post/readPost.html', checkType=curUser.checkType, len=len(result['commentList']),
                           userID=curUser.userID, isLogin=curUser.isLogin, userKey=curUser.userKey, post=post)


# 의뢰 게시글 삭제하기
@app.route(path + '/delete_post/<int:post_id>/<userKey>')
def delete_post(post_id, userKey):
    curUser.userKey = userKey
    curUser.isLogin = True
    curUser.userID = DB_findUser_key(userKey)
    curUser.user = DB_getUser(curUser.userID)
    if isHelper(curUser.userID):
        curUser.isHelper = True
        curUser.checkType = curUser.user.getHelperType()

    if curUser.userID == None:
        return redirect('/dev/login_page')

    deletePost(post_id)
    return redirect('/dev/post_board/1/' + userKey)


# 의뢰 게시글 수정하기
@app.route(path + '/modify_post/<int:post_id>/<userKey>', methods=['GET', 'POST'])
def modify_post_key(post_id, userKey):
    curUser.isLogin = True
    curUser.userID = DB_findUser_key(userKey)
    curUser.user = DB_getUser(curUser.userID)
    if isHelper(curUser.userID):
        curUser.isHelper = True
        curUser.checkType = curUser.user.getHelperType()

    if curUser.userID == None:
        return redirect('/dev/login_page')

    if request.method == 'GET':
        return redirect(url_for('modify_post', post_id=post_id))
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
        return redirect('/dev/post_board/1/' + userKey)


@app.route(path + '/modify_post/<int:post_id>', methods=['GET', 'POST'])
def modify_post(post_id):
    if curUser.userID == None:
        return redirect('/dev/login_page')

    post = getPost(post_id).__dict__
    post['_Post__address'] = post['_Post__address'].__dict__
    i = 0
    for element in post['commentList']:
        post['commentList'][i] = element.__dict__
        i += 1

    return render_template('Post/modify.html', checkType=curUser.checkType, userID=curUser.userID,
                           isLogin=curUser.isLogin, userKey=curUser.userKey, post=post)


# 댓글 삭제하기
@app.route(path + '/delete_comment/<int:post_id>/<int:comment_id>/<userKey>', methods=['GET', 'POST'])
def delete_comment(post_id, comment_id, userKey):
    curUser.userKey = userKey
    curUser.isLogin = True
    curUser.userID = DB_findUser_key(userKey)
    curUser.user = DB_getUser(curUser.userID)
    if isHelper(curUser.userID):
        curUser.isHelper = True
        curUser.checkType = curUser.user.getHelperType()

    if curUser.userID == None:
        return redirect('/dev/login_page')

    deleteComment(post_id, comment_id)

    return redirect(url_for('view_post', post_id=post_id, userKey=curUser.userKey))


# 의뢰 게시판 보기
@app.route(path + '/select_helper/', methods=['GET'])
def request_logout():
    return redirect('/dev/login_page')


@app.route(path + '/select_helper/<userKey>', methods=['GET'])
def request_matching(userKey):
    curUser.isLogin = True
    curUser.userID = DB_findUser_key(userKey)
    curUser.user = DB_getUser(curUser.userID)
    if isHelper(curUser.userID):
        curUser.isHelper = True
        curUser.checkType = curUser.user.getHelperType()

    if curUser.userID == None:
        return redirect('/dev/login_page')

    return render_template('Matching/newMatching.html', checkType=curUser.checkType, isLogin=curUser.isLogin,
                           userKey=userKey)


# 병원동행 도우미 신청
@app.route(path + '/accompany/<userKey>', methods=['GET', 'POST'])
def accompany_matching_key(userKey):
    curUser.userKey = userKey
    curUser.isLogin = True
    curUser.userID = DB_findUser_key(userKey)
    curUser.user = DB_getUser(curUser.userID)
    if isHelper(curUser.userID):
        curUser.isHelper = True
        curUser.checkType = curUser.user.getHelperType()

    if curUser.isLogin == False:
        return redirect('/dev/login_page')

    if request.method == 'POST':
        # userinfo = user.getUserInfo()
        reqDate = request.form['date'] + " " + request.form['time']
        # 출발지 주소
        address = request.form['address']
        start_addr = Address(address, "", "")
        # 병원 주소
        hospital_addr = Address(request.form['hospitalLoc'], request.form['hospital'], request.form['sido'])
        reason = request.form['reason']

        createAccompany(curUser.userID, reqDate, start_addr, hospital_addr, reason)
        curUser.user = DB_getUser(curUser.userID)

        matchingList = curUser.user.getMyRequest()
        matchingID = matchingList[-1]

        return redirect(url_for('check_request_userKey', helpType=HelperType.ACCOMPANY, matchingID=matchingID,
                                userKey=curUser.userKey))

    return redirect(url_for('accompany_matching'))


@app.route(path + '/accompany', methods=['GET', 'POST'])
def accompany_matching():
    if curUser.isLogin == False:
        render_template("login.html", checkType=curUser.checkType, isLogin=curUser.isLogin)
    return render_template("Matching/accompanyMatching.html", checkType=curUser.checkType, isLogin=curUser.isLogin,
                           userKey=curUser.userKey)


# 심리상담 도우미 요청
@app.route(path + '/counsel/<userKey>', methods=['GET', 'POST'])
def counsel_matching_key(userKey):
    curUser.userKey = userKey
    curUser.isLogin = True
    curUser.userID = DB_findUser_key(userKey)
    curUser.user = DB_getUser(curUser.userID)
    if isHelper(curUser.userID):
        curUser.isHelper = True
        curUser.checkType = curUser.user.getHelperType()

    if curUser.isLogin == False:
        return redirect('/dev/login_page')

    if request.method == 'POST':
        # userinfo = user.getUserInfo()
        reqDate = request.form['date'] + " " + request.form['time']
        addr = Address(request.form['address'] + " " + request.form['detailAddress'], "", request.form['sido'])
        category = request.form['category']

        createCounsel(curUser.userID, reqDate, addr, category)
        user = DB_getUser(curUser.userID)

        matchingList = user.getMyRequest()
        matchingID = matchingList[-1]

        return redirect(url_for('check_request_userKey', helpType=HelperType.COUNSEL, matchingID=matchingID,
                                userKey=curUser.userKey))
    return redirect(url_for('counsel_matching'))


@app.route(path + '/counsel', methods=['GET', 'POST'])
def counsel_matching():
    return render_template("Matching/counselMatching.html", checkType=curUser.checkType, isLogin=curUser.isLogin,
                           userKey=curUser.userKey)


# 안전점검 도우미 요청
@app.route(path + '/safe/<userKey>', methods=['GET', 'POST'])
def safe_matching_key(userKey):
    curUser.userKey = userKey
    curUser.isLogin = True
    curUser.userID = DB_findUser_key(userKey)
    curUser.user = DB_getUser(curUser.userID)
    if isHelper(curUser.userID):
        curUser.isHelper = True
        curUser.checkType = curUser.user.getHelperType()

    if curUser.isLogin == False:
        return redirect('/dev/login_page')

    if request.method == 'POST':
        # userinfo = user.getUserInfo()
        reqDate = request.form['date'] + " " + request.form['time']
        addr = Address(request.form['address'] + " " + request.form['detailAddress'], "", request.form['sido'])
        category = request.form['category']

        createSafetyCheck(curUser.userID, reqDate, addr, category)
        user = DB_getUser(curUser.userID)

        matchingList = user.getMyRequest()
        matchingID = matchingList[-1]

        return redirect(url_for('check_request_userKey', helpType=HelperType.SAFETYCHECK, matchingID=matchingID,
                                userKey=curUser.userKey))
    return redirect(url_for('safe_matching'))


@app.route(path + '/safe', methods=['GET', 'POST'])
def safe_matching():
    return render_template("Matching/safeMatching.html", checkType=curUser.checkType, isLogin=curUser.isLogin,
                           userKey=curUser.userKey)


@app.route(path + '/check_request/<int:helpType>/<int:matchingID>/<userKey>', methods=['GET', 'POST'])
def check_request_userKey(helpType, matchingID, userKey):
    curUser.userKey = userKey
    curUser.isLogin = True
    curUser.userID = DB_findUser_key(userKey)
    curUser.user = DB_getUser(curUser.userID)
    if isHelper(curUser.userID):
        curUser.isHelper = True
        curUser.checkType = curUser.user.getHelperType()

    if curUser.isLogin == False:
        render_template("login.html", checkType=curUser.checkType, isLogin=curUser.isLogin)

    if request.method == 'POST':
        # 신청 취소
        flash("매칭 신청이 완료되었습니다.")
        return redirect(url_for('home_userID', userKey=userKey))
    return redirect('/dev/check_request/' + str(helpType) + '/' + str(matchingID))


@app.route(path + '/check_request/<int:helpType>/<int:matchingID>', methods=['GET', 'POST'])
def check_request(helpType, matchingID):
    if curUser.isLogin == False:
        render_template("login.html", checkType=curUser.checkType, isLogin=curUser.isLogin)

    check = {}
    matching = getMatching(matchingID)
    check['username'] = curUser.user.getUserInfo().NAME
    # 작성자, 날짜, 장소, 상세 내용
    if type(matching) is Accompany:
        check['helpType'] = "병원동행"
        check['date'] = matching.getRequestDate()
        check[
            'address'] = "[출발지] " + matching.getAddress().detailAddress + " [병원위치] " + matching.getHospitalLocation().detailAddress
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

    return render_template('check.html', checkType=curUser.checkType, matchingID=matchingID, check=check,
                           isLogin=curUser.isLogin, userKey=curUser.userKey)


# 매칭 취소/삭제하기
@app.route(path + '/delete_matching/<int:matchingID>/<userKey>')
def delete_matching(matchingID, userKey):
    deleteMatching(matchingID)
    return redirect('/dev/' + userKey)


# 도우미 신청 목록 보기
@app.route(path + '/matching_board/<int:helperType>/<int:page>/<userKey>', methods=['GET'])
def matching_board_key(helperType, page, userKey):
    curUser.userKey = userKey
    curUser.isLogin = True
    curUser.userID = DB_findUser_key(userKey)
    curUser.user = DB_getUser(curUser.userID)
    if isHelper(curUser.userID):
        curUser.isHelper = True
        curUser.checkType = curUser.user.getHelperType()

    if curUser.isLogin == False:
        render_template("login.html", checkType=curUser.checkType, isLogin=curUser.isLogin)

    if (helperType == 0):
        flash("도우미만 해당 페이지에 접근할 수 있습니다.", 'error')
        return redirect(url_for('/dev/' + userKey))

    return redirect(url_for('matching_board', helperType=helperType, page=page))


@app.route(path + '/matching_board/<int:helperType>/<int:page>', methods=['GET'])
def matching_board(helperType, page):
    if curUser.isLogin == False:
        render_template("login.html", checkType=curUser.checkType, isLogin=curUser.isLogin)

    # 목록 리스트 불러오기
    page_list = getMatchingList(page, helperType)
    max_page = getAllMatchingPageCount(helperType)

    block_size = 5
    block_num = int((page - 1) / block_size)
    block_start = (block_size * block_num) + 1
    block_end = block_start + (block_size - 1)

    return render_template('Matching/matchingBoard.html', checkType=curUser.checkType,
                           page_list=page_list, max_page=max_page, this_page=page, start=block_start, end=block_end,
                           isLogin=curUser.isLogin, userKey=curUser.userKey)


# 개별 매칭 보기
@app.route(path + '/matching/<int:matching_id>/<userKey>', methods=['GET'])
def view_matching_key(matching_id, userKey):
    curUser.userKey = userKey
    curUser.isLogin = True
    curUser.userID = DB_findUser_key(userKey)
    curUser.user = DB_getUser(curUser.userID)
    if isHelper(curUser.userID):
        curUser.isHelper = True
        curUser.checkType = curUser.user.getHelperType()

    if curUser.isLogin == False:
        render_template("login.html", checkType=curUser.checkType, isLogin=curUser.isLogin)

    return redirect('/dev/matching/' + str(matching_id))


@app.route(path + '/matching/<int:matching_id>', methods=['GET'])
def view_matching(matching_id):
    # 매칭 내용 불러오기
    matching = getMatching(matching_id)

    matchingDict = matching.__dict__
    result = {}
    if type(matching) is Accompany:
        help = "병원동행 "
        result['matchingIdx'] = matchingDict['_Accompany__matchingIdx']
        result['reqDate'] = matchingDict['_Accompany__requestDate']
        result['address'] = matching.getAddress().__dict__
        result['hospitalLoc'] = matching.getHospitalLocation().__dict__
        result['contents'] = matchingDict['_Accompany__reason']
        result['helpeeID'] = matching.getHelpeeInfo().ID
    elif type(matching) is Counsel:
        help = "심리상담 "
        result['matchingIdx'] = matchingDict['_Counsel__matchingIdx']
        result['reqDate'] = matchingDict['_Counsel__requestDate']
        result['address'] = matching.getAddress().__dict__
        result['contents'] = matchingDict['_Counsel__category']
        result['helpeeID'] = matching.getHelpeeInfo().ID
    elif type(matching) is SafetyCheck:
        help = "안전점검 "
        result['matchingIdx'] = matchingDict['_SafetyCheck__matchingIdx']
        result['reqDate'] = matchingDict['_SafetyCheck__requestDate']
        result['address'] = matching.getAddress().__dict__
        result['contents'] = matchingDict['_SafetyCheck__checkPart']
        result['helpeeID'] = matching.getHelpeeInfo().ID

    return render_template('Matching/readMatching.html', checkType=curUser.checkType, helpType=curUser.checkType,
                           help=help, matching=result, isLogin=curUser.isLogin, userKey=curUser.userKey)


@app.route(path + '/consent_matching/<int:matchingID>/<userKey>')
def consent_matching(matchingID, userKey):
    curUser.userKey = userKey
    curUser.isLogin = True
    curUser.userID = DB_findUser_key(userKey)
    curUser.user = DB_getUser(curUser.userID)
    if isHelper(curUser.userID):
        curUser.isHelper = True
        curUser.checkType = curUser.user.getHelperType()

    requestMatching(matchingID, curUser.userID)
    # 메시지 전송 + 메시지 전송 예약
    return redirect('/dev/' + userKey)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        app.debug = True
        app.jinja_env.auto_reload = True
        app.config['TEMPLATES_AUTO_RELOAD'] = True
        app.run(host='0.0.0.0', port=4000)
    else:
        app.run(host='0.0.0.0')