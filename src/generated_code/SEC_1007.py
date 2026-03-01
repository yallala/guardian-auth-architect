import smtplib
import uuid

class AccessLogic:
    def __init__(self):
        self.verification_tokens = {}

    def initiate_password_reset(self, user_email, host, port, sender_email):
        token = str(uuid.uuid4())
        self.verification_tokens[token] = user_email
        verification_link = f"https://example.com/reset-password/{token}"
        msg = f"Subject: Password Reset Verification\n\nClick the link to verify your password reset request: {verification_link}"
        server = smtplib.SMTP(host, port)
        server.starttls()
        server.sendmail(sender_email, user_email, msg)
        server.quit()

    def verify_token(self, token):
        return self.verification_tokens.pop(token, None)