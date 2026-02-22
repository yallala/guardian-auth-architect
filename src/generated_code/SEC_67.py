def validate_corporate_email_domain(email: str, valid_domains: list) -> str:
    """
    Validates that the provided email belongs to the predefined corporate domains.

    :param email: The email address entered by the user.
    :param valid_domains: A list of valid corporate domains (e.g., ['@company.com', '@subsidiary.com']).
    :return: Success message if valid, or rejection message if invalid.
    """
    # Input validation
    if not isinstance(email, str) or not isinstance(valid_domains, list):
        raise ValueError("Invalid inputs. Ensure email is a string and valid_domains is a list.")

    # Check if the email matches any valid domain
    for domain in valid_domains:
        if email.endswith(domain):
            return f"Authentication successful for {email}."

    # Reject email if no valid domain is matched
    valid_domains_str = ", ".join(valid_domains)  # Formatting domains for error message
    return f"Please use your corporate email account ending with {valid_domains_str}."


# Test cases
if __name__ == "__main__":
    # Define valid domains
    corporate_domains = ["@company.com", "@subsidiary.com"]

    # Test case: Valid domain
    print(validate_corporate_email_domain("user@company.com", corporate_domains))  # Expected success message

    # Test case: Invalid domain
    print(validate_corporate_email_domain("user@hotmail.com", corporate_domains))  # Expected rejection message

    # Test case: Subdomain, not explicitly valid
    print(validate_corporate_email_domain("user@mail.company.com", corporate_domains))  # Expected rejection message

    # Test case: Another valid domain
    print(validate_corporate_email_domain("user@subsidiary.com", corporate_domains))  # Expected success message

    # Test case: Edge case with empty string
    print(validate_corporate_email_domain("", corporate_domains))  # Expected rejection message

    # Test case: Edge case with missing or malformed input
    try:
        print(validate_corporate_email_domain(None, corporate_domains))  # Expecting ValueError
    except ValueError as ve:
        print(ve)