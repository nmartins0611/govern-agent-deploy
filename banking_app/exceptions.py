"""Custom exceptions for the banking application"""


class BankingError(Exception):
    """Base exception for banking operations"""
    pass


class AccountNotFoundError(BankingError):
    """Raised when an account is not found"""
    pass


class InsufficientFundsError(BankingError):
    """Raised when an account has insufficient funds for a transaction"""
    pass


class InvalidAmountError(BankingError):
    """Raised when an invalid amount is provided"""
    pass


class InvalidAccountError(BankingError):
    """Raised when account validation fails"""
    pass
