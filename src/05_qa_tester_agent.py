import os
from dotenv import load_dotenv

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(base_dir, '.env'))

def validate_feature(ticket_key):
    safe_name = ticket_key.replace("-", "_")
    
    # BLANKET MOCK TEMPLATE - Covers both SMTP and SMTP_SSL
    template = f"""
import pytest
from unittest.mock import patch, MagicMock
import smtplib
from {safe_name} import AccessLogic

@patch('smtplib.SMTP_SSL')
@patch('smtplib.SMTP')
class Test{safe_name}:
    def setup_method(self, method):
        self.logic = AccessLogic()

    def test_verify_domain(self, mock_smtp, mock_ssl):
        assert self.logic.verify_domain("user@example.com") is True
        assert self.logic.verify_domain("user@hacker.com") is False

    def test_send_verified_code(self, mock_smtp, mock_ssl):
        # We pass both mocks so pytest is happy with the signature
        assert self.logic.send_verified_code("test@example.com", "1234") is True

    def test_validate_code(self, mock_smtp, mock_ssl):
        assert self.logic.validate_code("1234", "1234") is True
        assert self.logic.validate_code("1234", "5678") is False
"""
    path = os.path.join(base_dir, "src", "generated_code", f"test_{safe_name}.py")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f: f.write(template)
    return True