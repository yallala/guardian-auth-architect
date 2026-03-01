import smtplib
import ssl
import json
import os
import pytest
from unittest.mock import MagicMock, ANY
from SEC_1008 import AccessLogic

@pytest.fixture
def access_logic():
    return AccessLogic()

def test_send_verification_code_happy_path(access_logic):
    # Arrange
    email = "testuser@example.com"
    host = "smtp.example.com"
    port = 587
    sender = "admin@example.com"
    verification_code = "123456"

    smtplib.SMTP = MagicMock()  # Mock the smtplib.SMTP class
    mocked_smtp = smtplib.SMTP.return_value
    mocked_smtp.starttls = MagicMock()
    mocked_smtp.sendmail = MagicMock()
    mocked_smtp.quit = MagicMock()

    access_logic.verification_codes[email] = verification_code  # Pre-assign the code for test verification

    # Act
    access_logic.send_verification_code(email, host, port, sender)

    # Assert
    smtplib.SMTP.assert_called_once_with(host, port)
    mocked_smtp.starttls.assert_called_once()
    mocked_smtp.sendmail.assert_called_once_with(sender, email, ANY)  # Valid email with message containing the code
    mocked_smtp.quit.assert_called_once()

def test_verify_email_code_happy_path(access_logic):
    # Arrange
    email = "testuser@example.com"
    verification_code = "123456"
    access_logic.verification_codes[email] = verification_code  # Add the code to the internal dictionary

    # Act
    result = access_logic.verify_email_code(email, verification_code)

    # Assert
    assert result is True