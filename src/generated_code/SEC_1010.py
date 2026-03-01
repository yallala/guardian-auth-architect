import uuid
import time
import smtplib

class AccessLogic:
    def __init__(self):
        self.reset_tokens = {}

    def generate_reset_token(self, email, host, port, sender, recipient):
        token = str(uuid.uuid4())
        expiry_time = time.time() + 900  # 15 minutes
        self.reset_tokens[email] = {'token': token, 'expires_at': expiry_time, 'used': False}
        msg = f"Subject: Password Reset Token\n\nYour reset token is: {token}"
        
        server = smtplib.SMTP(host, port)
        server.starttls()
        server.sendmail(sender, recipient, msg)
        server.quit()
    
    def validate_reset_token(self, email, token):
        if email in self.reset_tokens:
            token_data = self.reset_tokens[email]
            if token_data['token'] == token and not token_data['used'] and time.time() < token_data['expires_at']:
                self.reset_tokens[email]['used'] = True
                return True
        return False