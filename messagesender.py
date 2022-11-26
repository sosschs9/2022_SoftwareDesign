import config
import matching
from twilio.rest import Client

class MessageSender:
    def sendMatching(matching):
        account_sid = config.twilio_account_sid
        auth_token = config.twilio_auth_token
        client = Client(account_sid, auth_token)
        _message = type(matching).__name__ + ' Accepted'
        message = client.messages.create(
            to = '+82' + PHONE_NUMBER,
            from_ = config.twilio_from_number,
            body = _message
        )

    def sendAppointment():
        pass