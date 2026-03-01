
import pytest
from unittest.mock import patch, MagicMock
import smtplib
from SEC_971 import AccessLogic

@patch('smtplib.SMTP_SSL')
@patch('smtplib.SMTP')
class TestSEC_971:
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
