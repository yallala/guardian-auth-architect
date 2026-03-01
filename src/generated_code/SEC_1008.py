import smtplib
import random
import re

class AccessLogic:
    def __init__(self):
        self.verification_codes = {}

    def send_verification_code(self, email, host, port, sender):
        # Generate a 6-digit verification code
        code = '{:06d}'.format(random.randint(0, 999999))
        
        # Associate the code with the specific email
        self.verification_codes[email] = code
        
        # Prepare and send the verification code email
        msg = f"Subject: Password Reset Verification Code\n\nYour code is: {code}"
        server = smtplib.SMTP(host, port)
        server.starttls()
        server.sendmail(sender, email, msg)
        server.quit()

    def verify_email_code(self, email, code):
        # Verify the code matches the email
        return self.verification_codes.get(email) == code

    def is_valid_email(self, email):
        # Validate email syntax using regular expression
        email_regex = re.compile(r"[^@]+@[^@]+\.[^@]+")
        return bool(email_regex.match(email))