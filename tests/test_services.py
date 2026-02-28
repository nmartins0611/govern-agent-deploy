"""Unit tests for banking services"""

import pytest
from banking_app.services import BankingService
from banking_app.exceptions import (
    AccountNotFoundError,
    InsufficientFundsError,
    InvalidAmountError,
    InvalidAccountError
)


class TestGetBalance:
    """Tests for get_balance service"""

    def test_get_balance_success(self, session, sample_accounts):
        """Test getting balance for existing account"""
        service = BankingService(session)
        result = service.get_balance(sample_accounts[0].id)

        assert result['account_id'] == sample_accounts[0].id
        assert result['account_number'] == sample_accounts[0].account_number
        assert result['holder_name'] == sample_accounts[0].holder_name
        assert result['balance'] == 1000.00
        assert result['currency'] == 'USD'
        assert 'timestamp' in result

    def test_get_balance_account_not_found(self, session):
        """Test getting balance for non-existent account"""
        service = BankingService(session)

        with pytest.raises(AccountNotFoundError):
            service.get_balance("non-existent-id")

    def test_get_balance_invalid_account_id(self, session):
        """Test getting balance with invalid account ID"""
        service = BankingService(session)

        with pytest.raises(InvalidAccountError):
            service.get_balance("")


class TestTransferFunds:
    """Tests for transfer_funds service"""

    def test_transfer_success(self, session, sample_accounts):
        """Test successful fund transfer"""
        service = BankingService(session)

        initial_from_balance = sample_accounts[0].balance
        initial_to_balance = sample_accounts[1].balance

        result = service.transfer_funds(
            from_account_id=sample_accounts[0].id,
            to_account_id=sample_accounts[1].id,
            amount=100.00,
            description="Test transfer"
        )

        # Refresh accounts from database
        session.refresh(sample_accounts[0])
        session.refresh(sample_accounts[1])

        assert result['amount'] == 100.00
        assert result['status'] == 'completed'
        assert result['description'] == "Test transfer"
        assert sample_accounts[0].balance == initial_from_balance - 100.00
        assert sample_accounts[1].balance == initial_to_balance + 100.00

    def test_transfer_insufficient_funds(self, session, sample_accounts):
        """Test transfer with insufficient funds"""
        service = BankingService(session)

        with pytest.raises(InsufficientFundsError):
            service.transfer_funds(
                from_account_id=sample_accounts[2].id,  # Has only 100.00
                to_account_id=sample_accounts[0].id,
                amount=200.00
            )

    def test_transfer_from_account_not_found(self, session, sample_accounts):
        """Test transfer with non-existent source account"""
        service = BankingService(session)

        with pytest.raises(AccountNotFoundError):
            service.transfer_funds(
                from_account_id="non-existent",
                to_account_id=sample_accounts[0].id,
                amount=50.00
            )

    def test_transfer_to_account_not_found(self, session, sample_accounts):
        """Test transfer with non-existent destination account"""
        service = BankingService(session)

        with pytest.raises(AccountNotFoundError):
            service.transfer_funds(
                from_account_id=sample_accounts[0].id,
                to_account_id="non-existent",
                amount=50.00
            )

    def test_transfer_invalid_amount_negative(self, session, sample_accounts):
        """Test transfer with negative amount"""
        service = BankingService(session)

        with pytest.raises(InvalidAmountError):
            service.transfer_funds(
                from_account_id=sample_accounts[0].id,
                to_account_id=sample_accounts[1].id,
                amount=-50.00
            )

    def test_transfer_invalid_amount_zero(self, session, sample_accounts):
        """Test transfer with zero amount"""
        service = BankingService(session)

        with pytest.raises(InvalidAmountError):
            service.transfer_funds(
                from_account_id=sample_accounts[0].id,
                to_account_id=sample_accounts[1].id,
                amount=0
            )

    def test_transfer_invalid_amount_too_many_decimals(self, session, sample_accounts):
        """Test transfer with too many decimal places"""
        service = BankingService(session)

        with pytest.raises(InvalidAmountError):
            service.transfer_funds(
                from_account_id=sample_accounts[0].id,
                to_account_id=sample_accounts[1].id,
                amount=50.123
            )


class TestGetTransactionHistory:
    """Tests for get_transaction_history service"""

    def test_get_transaction_history_success(self, session, sample_accounts, sample_transactions):
        """Test getting transaction history"""
        service = BankingService(session)

        result = service.get_transaction_history(sample_accounts[0].id)

        assert result['account_id'] == sample_accounts[0].id
        assert len(result['transactions']) == 2  # Account has 2 transactions
        assert result['pagination']['total'] == 2
        assert result['pagination']['page'] == 1

    def test_get_transaction_history_pagination(self, session, sample_accounts, sample_transactions):
        """Test transaction history pagination"""
        service = BankingService(session)

        result = service.get_transaction_history(
            sample_accounts[0].id,
            page=1,
            per_page=1
        )

        assert len(result['transactions']) == 1
        assert result['pagination']['total'] == 2
        assert result['pagination']['total_pages'] == 2

    def test_get_transaction_history_account_not_found(self, session):
        """Test getting transaction history for non-existent account"""
        service = BankingService(session)

        with pytest.raises(AccountNotFoundError):
            service.get_transaction_history("non-existent-id")

    def test_get_transaction_history_empty(self, session, sample_accounts):
        """Test getting transaction history for account with no transactions"""
        service = BankingService(session)

        result = service.get_transaction_history(sample_accounts[2].id)

        assert len(result['transactions']) == 0
        assert result['pagination']['total'] == 0
