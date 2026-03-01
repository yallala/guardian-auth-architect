import smtplib
import ssl
import json
import os
from SEC_1007 import AccessLogic
from unittest.mock import MagicMock, ANY
import smtplib

def test_initiate_password_reset_sends_email_with_verification_link():
    # Arrange
    access_logic = AccessLogic()
    user_email = 'user@example.com'
    host = 'smtp.example.com'
    port = 587
    sender_email = 'sender@example.com'

    # Mocking smtplib.SMTP and its methods
    mock_smtp = MagicMock()
    smtplib.SMTP = MagicMock(return_value=mock_smtp)

    # Act
    access_logic.initiate_password_reset(user_email, host, port, sender_email)

    # Assert
    smtplib.SMTP.assert_called_once_with(host, port)
    mock_smtp.starttls.assert_called_once()
    mock_smtp.sendmail.assert_called_once_with(
        sender_email, user_email, ANY  # The message contains the verification link
    )
    mock_smtp.quit.assert_called_once()


def test_verify_token_returns_email_and_removes_token():
    # Arrange
    access_logic = AccessLogic()
    user_email = 'user@example.com'
    token = 'mock_token_123'
    access_logic.verification_tokens[token] = user_email

    # Act
    result = access_logic.verify_token(token)

    # Assert
    assert result == user_email
    assert token not in access_logic.verification_tokens