"""Input validation utilities"""

import re
from banking_app.exceptions import InvalidAmountError, InvalidAccountError


def validate_amount(amount):
    """
    Validate transaction amount

    Args:
        amount: Amount to validate

    Raises:
        InvalidAmountError: If amount is invalid

    Returns:
        float: Validated amount
    """
    try:
        amount_float = float(amount)
    except (ValueError, TypeError):
        raise InvalidAmountError("Amount must be a valid number")

    if amount_float <= 0:
        raise InvalidAmountError("Amount must be positive")

    # Check for max 2 decimal places
    if round(amount_float, 2) != amount_float:
        raise InvalidAmountError("Amount can have maximum 2 decimal places")

    return amount_float


def validate_account_id(account_id):
    """
    Validate account ID format

    Args:
        account_id: Account ID to validate

    Raises:
        InvalidAccountError: If account ID is invalid

    Returns:
        str: Validated account ID
    """
    if not account_id or not isinstance(account_id, str):
        raise InvalidAccountError("Account ID must be a non-empty string")

    account_id = account_id.strip()

    if not account_id:
        raise InvalidAccountError("Account ID cannot be empty")

    return account_id


def validate_pagination(page, per_page):
    """
    Validate pagination parameters

    Args:
        page: Page number
        per_page: Items per page

    Returns:
        tuple: (validated_page, validated_per_page)
    """
    try:
        page = int(page) if page else 1
        per_page = int(per_page) if per_page else 10
    except (ValueError, TypeError):
        page = 1
        per_page = 10

    page = max(1, page)
    per_page = min(max(1, per_page), 100)  # Max 100 items per page

    return page, per_page
