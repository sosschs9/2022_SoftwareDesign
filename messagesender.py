import config
import matching
from twilio.rest import Client

class MessageSender:
    def to_helpee_Form(address, date, username, phoneNumber, helptype):
        message = ["[해줌] 도우미 매칭 완료", 
        f"{username}님! 신청하신 도우미 요청에 대해 매칭이 완료되었습니다.\n", 

        "✅ 신청 상세 내용:", 
        f"- {helptype} 도우미 요청",
        f"- 위치: {address}",
        f"- 날짜 및 시간: {date}\n",

        "✅ 도우미 연락처:",
        f"{phoneNumber}\n",

        "* 위 연락처를 통해 도우미와 연락을 취하시기 바랍니다.",
        "* 이외 궁금하신 점은 고객센터로 연락바랍니다.\n",

        "📞 고객센터:",
        "0110-1236"]
        return '\n'.join(message)

    def to_helper_Form(address, date, username, phoneNumber, helptype):
        message = ["[해줌] 도우미 매칭 완료", 
        f"{username}님! 승낙하신 도우미 요청에 대해 매칭이 완료되었습니다.\n", 

        "✅ 신청 상세 내용:", 
        f"- {helptype} 도우미 요청",
        f"- 위치: {address}",
        f"- 날짜 및 시간: {date}\n",

        "✅ 신청자 연락처:",
        f"{phoneNumber}\n",

        "* 위 연락처를 통해 신청자와 연락을 취하시기 바랍니다.",
        "* 이외 궁금하신 점은 고객센터로 연락바랍니다.\n",

        "📞 고객센터:",
        "0110-1236"]
        return '\n'.join(message)
    
    def sendMatching(matching, helperInfo, helpeeInfo, helptype):
        account_sid = config.twilio_account_sid
        auth_token = config.twilio_auth_token
        client = Client(account_sid, auth_token)
        to_helper_message = MessageSender.to_helper_Form(matching.getAddress(), matching.getDate(), helperInfo[1], helpeeInfo[2], helptype)
        to_helpee_message = MessageSender.to_helpee_Form(matching.getAddress(), matching.getDate(), helpeeInfo[1], helperInfo[2], helptype)
        to_helper = client.messages.create(
            to = '+82' + helperInfo[2],
            from_ = config.twilio_from_number,
            body = to_helper_message
        )
        to_helpee = client.messages.create(
            to = '+82' + helpeeInfo[2],
            from_ = config.twilio_from_number,
            body = to_helpee_message
        )

    def sendAppointment():
        pass