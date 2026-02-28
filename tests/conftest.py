"""Pytest fixtures and configuration"""

import pytest
from banking_app.app import create_app
from banking_app.database import init_db
from banking_app.models import Account, Transaction, TransactionType, TransactionStatus


@pytest.fixture(scope='function')
def app():
    """Create application for testing"""
    test_config = {
        'TESTING': True,
    }

    app = create_app(test_config)

    # Use in-memory database for tests
    app.db_session = init_db('sqlite:///:memory:')

    yield app

    # Cleanup
    app.db_session.remove()


@pytest.fixture(scope='function')
def client(app):
    """Create test client"""
    return app.test_client()


@pytest.fixture(scope='function')
def session(app):
    """Get database session for tests"""
    session = app.db_session()
    yield session
    session.close()


@pytest.fixture(scope='function')
def sample_accounts(session):
    """Create sample accounts for testing"""
    accounts = [
        Account(
            id="test-account-1",
            account_number="TEST001",
            holder_name="Test User 1",
            balance=1000.00,
            currency="USD"
        ),
        Account(
            id="test-account-2",
            account_number="TEST002",
            holder_name="Test User 2",
            balance=500.00,
            currency="USD"
        ),
        Account(
            id="test-account-3",
            account_number="TEST003",
            holder_name="Test User 3",
            balance=100.00,
            currency="USD"
        ),
    ]

    session.add_all(accounts)
    session.commit()

    return accounts


@pytest.fixture(scope='function')
def sample_transactions(session, sample_accounts):
    """Create sample transactions for testing"""
    transactions = [
        Transaction(
            from_account_id=sample_accounts[0].id,
            to_account_id=sample_accounts[1].id,
            amount=50.00,
            transaction_type=TransactionType.TRANSFER,
            status=TransactionStatus.COMPLETED,
            description="Test transfer 1"
        ),
        Transaction(
            from_account_id=sample_accounts[1].id,
            to_account_id=sample_accounts[0].id,
            amount=25.00,
            transaction_type=TransactionType.TRANSFER,
            status=TransactionStatus.COMPLETED,
            description="Test transfer 2"
        ),
    ]

    session.add_all(transactions)
    session.commit()

    return transactions
