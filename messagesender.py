import config
import matching
from datetime import date, timedelta
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

    def Appointment_Form(address, date, username, helptype):
        message = ["[해줌] 재신청 권유 알림",
        f"{username}님! 귀하의 도우미 신청 내역에 대해 재신청 기간으로 확인되어 권유 안내 드립니다.\n",

        "✅ 신청 내역:",
        f"- {helptype} 도우미 요청",
        f"- 위치: {address}",
        f"- 날짜 및 시간: {date}",

        "✅ 해줌 사이트에서 내역 확인하시고, 재신청 부탁드립니다!\n"

        "* 재신청 권유 알림은 해당 신청 내역에 대해 1회만 발송됩니다."
        "* 이외 궁금하신 점은 고객센터로 문의 부탁드립니다."

        "📞 고객센터:"
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

    def sendAppointment(matching, helperInfo, helpeeInfo, helptype):
        period = timedelta(weeks=3)
        if date.today() == datetime.datetime.strptime(matching.getDate(), '%Y년 %m월 %d일 %H:%M').date() + period :
            account_sid = config.twilio_account_sid
            auth_token = config.twilio_auth_token
            client = Client(account_sid, auth_token)
            sendForm = Appointment_Form(matching.getAddress(), matching.getDate(), helperInfo[1], helptype)
            to_helper = client.messages.create(
                to = '+82' + helperInfo[2],
                from_ = config.twilio_from_number,
                body = to_helper_message
            )
            sendForm = Appointment_Form(matching.getAddress(), matching.getDate(), helpeeInfo[1], helptype)
            to_helpe3 = client.messages.create(
                to = '+82' + helpeeInfo[2],
                from_ = config.twilio_from_number,
                body = to_helper_message
            )
        else pass