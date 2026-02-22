import pytest
import sys
import os

# 1. FIX THE PATH: Tell Python to look in the current folder for the source code
sys.path.append(os.path.dirname(__file__))

# 2. FIX THE IMPORT: Match the implementation filename and function name
from SEC_67 import validate_corporate_email_domain

class TestValidateCorporateEmailDomain:

    # Positive Test: Valid corporate email
    def test_valid_corporate_email(self):
        email = "john.doe@company.com"
        domains = ["company.com", "subsidiary.com"]
        # Use startswith to handle extra text like "... for john.doe@company.com"
        result = validate_corporate_email_domain(email, domains)
        assert result.startswith("Authentication successful")

    # Negative Test: Invalid non-corporate domain
    def test_invalid_email_domain(self):
        email = "user@hotmail.com"
        domains = ["company.com", "subsidiary.com"]
        # Partial match ensures the core security message is present
        assert "Please use your corporate email account" in validate_corporate_email_domain(email, domains)

    # Edge Case: Empty string input
    def test_empty_email_string(self):
        email = ""
        domains = ["company.com", "subsidiary.com"]
        # Validates that the system denies access for empty inputs
        result = validate_corporate_email_domain(email, domains)
        assert "Please use your corporate email" in result or "Invalid" in result

    # Positive Test: Secondary corporate domain
    def test_valid_alternate_corporate_domain(self):
        email = "user@subsidiary.com"
        domains = ["company.com", "subsidiary.com"]
        assert validate_corporate_email_domain(email, domains).startswith("Authentication successful")