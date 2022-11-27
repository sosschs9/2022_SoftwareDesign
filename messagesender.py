import config
import matching
from twilio.rest import Client

class MessageSender:
    def messageForm(username, helptype, address, date, phoneNumber):
        message = ["[해줌] 도우미 매칭 완료", 
        f"{username}님! 신청하신 도우미 요청에 대해 매칭이 완료되었습니다.\n", 

        "신청 상세 내용:", 
        f"- {helptype} 도우미 요청",
        f"- 위치: {address}",
        f"- 날짜 및 시간: {date}\n",

        "도우미 연락처:",
        f"{phoneNumber}\n",

        "* 위 연락처를 통해 매칭된 도우미와 연락 어쩌구",
        "* 이외 궁금하신 점은 고객센터로 연락바랍니다.\n",

        "고객센터:",
        "0110-1236"]
        return '\n'.join(message)
    
    def sendMatching(matching):
        account_sid = config.twilio_account_sid
        auth_token = config.twilio_auth_token
        client = Client(account_sid, auth_token)
        _message = MessageSender.messageForm("OO시 OO구 OO로", "2022년 11월 30일 17:50", "010-xxxx-xxxx")
        message = client.messages.create(
            to = '+82' + '01022551875',
            from_ = config.twilio_from_number,
            body = _message
        )

    def sendAppointment():
        pass