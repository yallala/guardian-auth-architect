import smtplib

class AccessLogic:
    def __init__(self, host, port, sender_email, recipient_email):
        self.host = host
        self.port = port
        self.sender_email = sender_email
        self.recipient_email = recipient_email

    def send_reset_code(self, reset_code):
        msg = f"Subject: Password Reset Code\n\nYour password reset code is: {reset_code}"
        server = smtplib.SMTP(self.host, self.port)
        server.starttls()
        server.sendmail(self.sender_email, self.recipient_email, msg)
        server.quit()