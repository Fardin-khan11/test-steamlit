import re

def is_valid_password(password: str) -> bool:
    """Check if password is at least 6 characters."""
    return len(password) >= 6

def is_valid_username(username: str) -> bool:
    """Check if username is at least 3 characters and alphanumeric."""
    return len(username) >= 3 and username.isalnum()
