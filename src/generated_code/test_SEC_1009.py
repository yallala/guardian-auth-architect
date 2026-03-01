import smtplib
import ssl
import json
import os
import pytest
from unittest.mock import MagicMock, ANY
from SEC_1009 import AccessLogic

def test_send_verification_email():
    # Mock the smtplib.SMTP object
    mock_smtp = MagicMock()
    smtplib.SMTP = MagicMock(return_value=mock_smtp)
    
    # Initialize AccessLogic
    access = AccessLogic()

    # Test data
    host = "smtp.email.com"
    port = 587
    sender = "sender@example.com"
    recipient = "recipient@example.com"
    callback_url = "http://localhost/verify"

    # Call the method
    access.send_verification_email(host, port, sender, recipient, callback_url)

    # Assertions to verify SMTP object interaction
    smtplib.SMTP.assert_called_once_with(host, port)
    mock_smtp.starttls.assert_called_once()
    mock_smtp.sendmail.assert_called_once_with(sender, recipient, ANY)
    mock_smtp.quit.assert_called_once()

def test_handle_verification_request():
    # Initialize AccessLogic
    access = AccessLogic()

    # Prepare test data
    recipient = "recipient@example.com"
    token = "testtoken123"
    access.pending_verifications[token] = recipient  # Manually set for testing

    # Call the method
    access.handle_verification_request(token)

    # Assertions
    assert token not in access.pending_verifications
    assert recipient in access.reset_codes
    assert access.reset_codes[recipient] is not None