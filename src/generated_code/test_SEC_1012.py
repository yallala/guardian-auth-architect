import smtplib
import ssl
import json
import os
import pytest
from unittest.mock import MagicMock, ANY
from SEC_1012 import AccessLogic


@pytest.fixture
def access_logic():
    return AccessLogic()


def test_send_password_reset_email_happy_path(access_logic, mocker):
    # Arrange
    mock_smtp = mocker.patch('smtplib.SMTP', autospec=True)
    mock_server = mock_smtp.return_value

    host = "smtp.example.com"
    port = 587
    sender = "sender@example.com"
    recipient = "recipient@example.com"
    msg = "Your password reset code is 123456."

    # Act
    access_logic.send_password_reset_email(host, port, sender, recipient, msg)

    # Assert
    mock_smtp.assert_called_once_with(host, port)  # Ensure SMTP server is instantiated with correct host and port
    mock_server.starttls.assert_called_once_with()  # Verify starttls is called to secure communication
    mock_server.sendmail.assert_called_once_with(sender, recipient, msg)  # Ensure the email is sent correctly
    mock_server.quit.assert_called_once_with()  # Confirm server is properly closed