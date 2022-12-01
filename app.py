import requests
from flask import Flask, render_template, request

app = Flask(__name__)

# default user 불러오기

# 메인페이지
@app.route('/')
def home():
    return render_template("main.html")

# 의뢰 게시판 보기
@app.route('/post_board', methods=['GET'])
def post_board():
    # 게시판 리스트 불러오기
    return render_template('Post/postBoard.html')

# 의뢰 게시글 작성하기
@app.route('/write_post', methods=['GET', 'POST'])
def writing_post():
    if request.method == 'POST':

        return render_template('Post/postBoard.html')
    else:
        return render_template('Post/newPost.html')

# 의뢰 게시글 보기
@app.route('/post/{id}', methods=['GET', 'POST'])
def view_post():
    # 게시글 불러오기

    if request.method == 'POST':
        # 댓글 작성
        return render_template('Post/readPost.html')
    else:
        return render_template('Post/newPost.html')

# 도우미 매칭
@app.route('/select_helper', methods=['GET'])
def request_matching():
    return render_template('Matching/newMatching.html')

@app.route('/select_helper/accompany', methods=['GET', 'POST'])
def accompany_matching():
    if request.method == 'POST':
        # 유저 정보 불러오기

        return render_template('check.html')
    else:
        return render_template("Matching/accompanyMatching.html")

@app.route('/select_helper/counsel', methods=['GET', 'POST'])
def counsel_matching():
    if request.method == 'POST':
        # 유저 정보 불러오기

        return render_template('check.html')
    else:
        return render_template("Matching/counselMatching.html")

@app.route('/select_helper/safe', methods=['GET', 'POST'])
def safe_matching():
    if request.method == 'POST':
        # 유저 정보 불러오기

        return render_template('check.html')
    else:
        return render_template("Matching/safeMatching.html")

# 도우미 신청 목록 보기
@app.route('/matching_board', methods=['GET'])
def matching_board():
    # 목록 리스트 불러오기
    return render_template('Matching/matchingBoard.html')

# 개별 매칭 보기
@app.route('/matching/{id}', methods=['GET'])
def view_matching():
    # 매칭 내용 불러오기
    return render_template('Matching/readMatching.html')


if __name__ == '__main__':
    app.run()
