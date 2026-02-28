"""Database initialization and seeding"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from banking_app.models import Base, Account, Transaction, TransactionType, TransactionStatus
import os


def get_database_url():
    """Get database URL from environment or use default"""
    return os.getenv('DATABASE_URL', 'sqlite:///banking.db')


def init_db(database_url=None):
    """Initialize database and return session factory"""
    if database_url is None:
        database_url = get_database_url()

    engine = create_engine(database_url, echo=False)
    Base.metadata.create_all(engine)

    session_factory = sessionmaker(bind=engine)
    Session = scoped_session(session_factory)

    return Session


def seed_data(Session):
    """Seed the database with sample accounts"""
    session = Session()

    # Check if already seeded
    if session.query(Account).count() > 0:
        session.close()
        return

    # Create sample accounts
    accounts = [
        Account(
            account_number="ACC001",
            holder_name="Alice Johnson",
            balance=5000.00,
            currency="USD"
        ),
        Account(
            account_number="ACC002",
            holder_name="Bob Smith",
            balance=3500.50,
            currency="USD"
        ),
        Account(
            account_number="ACC003",
            holder_name="Charlie Davis",
            balance=10000.75,
            currency="USD"
        ),
        Account(
            account_number="ACC004",
            holder_name="Diana Prince",
            balance=7200.25,
            currency="USD"
        ),
        Account(
            account_number="ACC005",
            holder_name="Eve Martinez",
            balance=1500.00,
            currency="USD"
        ),
    ]

    session.add_all(accounts)
    session.commit()
    session.close()

    print(f"Database seeded with {len(accounts)} accounts")
