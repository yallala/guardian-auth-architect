import smtplib
import ssl
import json
import os
import pytest
from unittest.mock import MagicMock, ANY
from SEC_1010 import AccessLogic

# Happy-path test case: Generation of reset token.
def test_generate_reset_token():
    # Setup
    access_logic = AccessLogic()
    email = "test@example.com"
    smtp_host = "smtp.example.com"
    smtp_port = 587
    sender_email = "sender@example.com"
    recipient_email = "recipient@example.com"

    # Mock smtplib.SMTP
    mock_smtp = MagicMock()
    smtplib.SMTP = MagicMock(return_value=mock_smtp)

    # Call the method
    access_logic.generate_reset_token(email, smtp_host, smtp_port, sender_email, recipient_email)

    # Assertions
    assert email in access_logic.reset_tokens
    token_data = access_logic.reset_tokens[email]
    assert 'token' in token_data and 'expires_at' in token_data and 'used' in token_data
    assert not token_data['used']
    mock_smtp.starttls.assert_called_once()
    mock_smtp.sendmail.assert_called_once_with(sender_email, recipient_email, ANY)
    mock_smtp.quit.assert_called_once()

# Happy-path test case: Validating reset token.
def test_validate_reset_token():
    # Setup
    access_logic = AccessLogic()
    email = "test@example.com"
    token = "abc123"
    expiry_time = time.time() + 900  # Expiry time (15 minutes from now)
    access_logic.reset_tokens[email] = {'token': token, 'expires_at': expiry_time, 'used': False}
    
    # Call the method
    is_valid = access_logic.validate_reset_token(email, token)

    # Assertions
    assert is_valid is True
    assert access_logic.reset_tokens[email]['used'] is True