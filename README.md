# 해줌 (help zoom)
*Member: 김동윤, 김주형, 송혜경, 장우석, 제유나*
<br><br>

## 1. 서비스 개요
행정안전부가 발간한 ‘2022 행정안전통계연보’에 따르면 1인 가구의 비중이 점차 늘어나고 있는 추세이다. 증가하는 1인 가구에 의해 사회에는 긍정적인 변화와 부정적인 변화가 생겨나고 있다. 이러한 사회적 변화에 맞춰 1인 가구의 생활패턴을 고려한 맞춤형 서비스 지원이 필요한 시기이다. 

 1인 가구의 가장 큰 특징은 혼자이고 특히, 청년층 1인 가구의 경우 직장 등으로 인해 집을 비우는 시간이 길다. 따라서 반려동·식물을 키우는 경우 관리에 문제가 생길 수 있다. 또한, 가구 설치나 시설 고장 등을 처리하는 것이 혼자 하기에는 어려운 점이 있다. 이러한 문제를 이웃끼리 서로서로 도와주자는 의미에서 이웃간 커뮤니티가 필요하다고 느꼈다.
<br><br><br>

## 2. 주요기능 요구사항
> 의뢰 게시판
- 의뢰 게시판 페이지에 들어가면 근처 주민들이 올린 게시글을 최신순으로 1페이지 당 20개씩 볼 수 있다. 목록에서 글의 제목을 클릭하면 게시글의 자세한 내용을 확인할 수 있으며, 진행하고 싶은 의뢰가 있다면 댓글을 달거나 게시글에 포함된 연락 방법으로 직접 연락할 수 있다. 
- 게시판을 통해 의뢰 게시글을 작성할 수 있으며, 정해진 양식인 제목, 의뢰 내용, 위치, 날짜, 연락 방법, 보수를 반드시 작성해야 한다. 사용자는 본인의 게시글과 댓글을 수정 및 삭제할 수 있지만 복구는 불가능하다.

> 도우미 매칭
- 신청자는 병원동행, 심리상담, 안전점검 중 하나에 대해 도우미를 요청할 수 있다. 각 도움 분야에 따라 추가적인 정보를 입력해 매칭을 신청하고, 요청 승낙 이전에는 신청을 취소할 수 있지만, 수정 및 복구는 불가능하다.
- 각 도우미는 본인의 분야에 맞는 도움 요청을 1페이지 당 20개씩 볼 수 있다. 목록에서 요청 내용을 클릭하면 자세한 내용을 확인할 수 있으며, 원하는 요청을 버튼을 통해 승낙할 수 있다.
- 매칭 완료 이후에는 신청자와 도우미에게 신청 정보 및 서로의 연락처를 문자메시지로 전송한다. 심리상담/안전점검 도움 요청일 경우, 신청자에게 매칭 완료 1달 이후에 메시지로 재신청 권유 알림을 보낸다.
<br><br><br>

## 3. 활용 기술
> Object-Oriented Systems Analysis & Designd

- usecase diagram, activity diagram, class diagram, Package Diagram, Sequence Diagram

> Front

- html, css, JS
- 도로명주소 API

> Back

- Flask(python) 기반 Serverless 애플리케이션 + AWS lambda(배포)
- Database: MongoDB(user, post, matching data 저장)
- Twilio: 메시지 전송 API
<br><br><br>


## 4. 실행방법
### 4-1. 배포 페이지 접속
[해줌 (help zoom)](https://url.kr/uo8rym).

![image](https://user-images.githubusercontent.com/81686317/205733882-183c9390-7bb1-4b58-a957-680482345ea3.png)
<br><br>
### 4-2. 로컬실행
> 로컬 실행 시 필요한 설정

**pip install -r requirements.txt**

```
certifi==2022.9.24
charset-normalizer==2.1.1
click==8.1.3
colorama==0.4.6
config==0.5.1
dnspython==2.2.1
Flask==2.2.2
idna==3.4
importlib-metadata==5.0.0
itsdangerous==2.1.2
Jinja2==3.1.2
MarkupSafe==2.1.1
PyJWT==2.6.0
pymongo==4.3.3
pytz==2022.6
requests==2.28.1
twilio==7.15.4
urllib3==1.26.12
Werkzeug==2.2.2
zipp==3.10.0
```
> 실행 방법

**flask run** or **python app.py** 실행 후 
**'실행url/dev'로 접속** _ex) 127.0.0.1:50000/dev_
<br><br>

### 4-3. 사이트 로그인

> 일반 사용자
- 아이디: user1~8 / 비밀번호: 1234

> 도우미
- 아이디: helper1~7 / 비밀번호: abcd
- 도우미유형(비트마스킹) >>  1(동행), 2(상담), 4(안전)

도우미 유형과 일치하는 요청만 목록에서 확인할 수 있음.
```
helper1: 병원동행
helper2: 심리상담
helper3: 병원동행 + 심리상담
helper4: 안전점검
helper5: 병원동행 + 안전점검
helper6: 심리상담 + 안전점검
helper7: 병원동행 + 심리상담 + 안전점검 
```
<br><br><br>

## 5. 팀원 역할

|이름|역할|
|---|------------------------|
|김동윤|__Back__<br>Post package(Writing/Post/Comment class) 구현|
|김주형|__Back__<br>User package(User/Helper class) 구현|
|송혜경|__Front/Back__<br>Interface 디자인 및 구현, UI Method 구현|
|장우석|__Back__<br>Matching package(Matching class 및 messegeSender) 구현|
|제유나|__Front/Back/DB__<br>DB, Interface 및 UI Method 구현, 병합 및 배포|

<br><br><br>
## 6. Notion
노션을 통해 자세한 요구사항 정의문서를 확인하실 수 있습니다.

[10조 노션링크](https://productive-sink-04a.notion.site/10-_-_-8aab670b594b46c7a837febc942c17a8).
