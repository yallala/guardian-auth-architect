import smtplib
import secrets
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

class AccessLogic:
    def __init__(self):
        self.pending_verifications = {}
        self.reset_codes = {}

    def send_verification_email(self, host, port, sender, recipient, callback_url):
        verification_token = secrets.token_hex(16)
        self.pending_verifications[verification_token] = recipient
        msg = f"Subject: Email Verification\n\nClick the link to verify your email: {callback_url}?token={verification_token}"
        server = smtplib.SMTP(host, port)
        server.starttls()
        server.sendmail(sender, recipient, msg)
        server.quit()

    def handle_verification_request(self, token):
        email = self.pending_verifications.pop(token, None)
        if email:
            reset_code = secrets.token_hex(3)
            self.reset_codes[email] = reset_code

    def get_reset_code(self, email):
        return self.reset_codes.get(email)

# Example implementation of the HTTP callback server (only for class logic demonstration)
class VerificationHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)
        token = query_params.get('token', [None])[0]
        if token:
            AccessLogic().handle_verification_request(token)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Email verified.")
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Invalid request.")

# Note: This code does not execute anything directly outside of the class or server handler.