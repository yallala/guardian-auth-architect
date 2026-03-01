import smtplib

class AccessLogic:
    def send_password_reset_email(self, host, port, sender, recipient, msg):
        server = smtplib.SMTP(host, port)
        server.starttls()
        server.sendmail(sender, recipient, msg)
        server.quit()