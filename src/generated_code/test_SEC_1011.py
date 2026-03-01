import smtplib
import ssl
import json
import os
import pytest
from unittest.mock import MagicMock, ANY
from SEC_1011 import AccessLogic

def test_send_reset_code_happy_path():
    # Arrange: Set up the AccessLogic object and mock SMTP
    host = "smtp.example.com"
    port = 587  # Default for TLS
    sender_email = "sender@example.com"
    recipient_email = "recipient@example.com"
    reset_code = "123456"
    mock_smtp = MagicMock()  # Create a mocked SMTP object

    def mock_smtp_init(host, port):
        assert host == "smtp.example.com"
        assert port == 587
        return mock_smtp

    smtplib.SMTP = MagicMock(side_effect=mock_smtp_init)  # Replace SMTP constructor with our mock version
    mock_smtp.starttls = MagicMock()
    mock_smtp.sendmail = MagicMock()
    mock_smtp.quit = MagicMock()

    access_logic = AccessLogic(host, port, sender_email, recipient_email)

    # Act: Call the send_reset_code method
    access_logic.send_reset_code(reset_code)

    # Assert: Verify that the SMTP methods were called in the correct order with expected arguments
    smtplib.SMTP.assert_called_once_with(host, port)
    mock_smtp.starttls.assert_called_once()
    mock_smtp.sendmail.assert_called_once_with(sender_email, recipient_email, ANY)
    mock_smtp.quit.assert_called_once()