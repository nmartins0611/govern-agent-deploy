"""Business logic for banking operations"""

from datetime import datetime, timezone
from sqlalchemy.exc import SQLAlchemyError
from banking_app.models import Account, Transaction, TransactionType, TransactionStatus
from banking_app.exceptions import (
    AccountNotFoundError,
    InsufficientFundsError,
    InvalidAmountError
)
from banking_app.validators import validate_amount, validate_account_id, validate_pagination


class BankingService:
    """Service class for banking operations"""

    def __init__(self, session):
        """
        Initialize banking service

        Args:
            session: SQLAlchemy session
        """
        self.session = session

    def get_balance(self, account_id):
        """
        Get account balance

        Args:
            account_id: Account identifier

        Returns:
            dict: Account balance information

        Raises:
            AccountNotFoundError: If account not found
        """
        account_id = validate_account_id(account_id)

        account = self.session.query(Account).filter_by(id=account_id).first()

        if not account:
            raise AccountNotFoundError(f"Account {account_id} not found")

        return {
            "account_id": account.id,
            "account_number": account.account_number,
            "holder_name": account.holder_name,
            "balance": round(account.balance, 2),
            "currency": account.currency,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    def transfer_funds(self, from_account_id, to_account_id, amount, description=None):
        """
        Transfer funds between accounts

        Args:
            from_account_id: Source account ID
            to_account_id: Destination account ID
            amount: Amount to transfer
            description: Optional transaction description

        Returns:
            dict: Transaction information

        Raises:
            AccountNotFoundError: If either account not found
            InsufficientFundsError: If source account has insufficient funds
            InvalidAmountError: If amount is invalid
        """
        from_account_id = validate_account_id(from_account_id)
        to_account_id = validate_account_id(to_account_id)
        amount = validate_amount(amount)

        # Begin transaction
        try:
            # Get accounts with row locking for concurrent safety
            from_account = self.session.query(Account).filter_by(
                id=from_account_id
            ).with_for_update().first()

            to_account = self.session.query(Account).filter_by(
                id=to_account_id
            ).with_for_update().first()

            if not from_account:
                raise AccountNotFoundError(f"Source account {from_account_id} not found")

            if not to_account:
                raise AccountNotFoundError(f"Destination account {to_account_id} not found")

            # Check sufficient funds
            if from_account.balance < amount:
                raise InsufficientFundsError(
                    f"Insufficient funds in account {from_account.account_number}. "
                    f"Available: {from_account.balance}, Required: {amount}"
                )

            # Create transaction record
            transaction = Transaction(
                from_account_id=from_account_id,
                to_account_id=to_account_id,
                amount=amount,
                transaction_type=TransactionType.TRANSFER,
                status=TransactionStatus.PENDING,
                description=description
            )
            self.session.add(transaction)

            # Update balances
            from_account.balance -= amount
            to_account.balance += amount

            # Mark transaction as completed
            transaction.status = TransactionStatus.COMPLETED

            # Commit transaction
            self.session.commit()

            return {
                "transaction_id": transaction.id,
                "from_account": from_account.account_number,
                "to_account": to_account.account_number,
                "amount": round(amount, 2),
                "status": transaction.status.value,
                "description": description,
                "timestamp": transaction.created_at.isoformat()
            }

        except (AccountNotFoundError, InsufficientFundsError, InvalidAmountError):
            self.session.rollback()
            raise
        except SQLAlchemyError as e:
            self.session.rollback()
            raise Exception(f"Database error during transfer: {str(e)}")

    def get_transaction_history(self, account_id, page=1, per_page=10,
                               transaction_type=None, start_date=None, end_date=None):
        """
        Get transaction history for an account

        Args:
            account_id: Account identifier
            page: Page number (default: 1)
            per_page: Items per page (default: 10)
            transaction_type: Filter by transaction type (optional)
            start_date: Filter transactions after this date (optional)
            end_date: Filter transactions before this date (optional)

        Returns:
            dict: Paginated transaction history

        Raises:
            AccountNotFoundError: If account not found
        """
        account_id = validate_account_id(account_id)
        page, per_page = validate_pagination(page, per_page)

        # Verify account exists
        account = self.session.query(Account).filter_by(id=account_id).first()
        if not account:
            raise AccountNotFoundError(f"Account {account_id} not found")

        # Build query
        query = self.session.query(Transaction).filter(
            (Transaction.from_account_id == account_id) |
            (Transaction.to_account_id == account_id)
        )

        # Apply filters
        if transaction_type:
            query = query.filter(Transaction.transaction_type == transaction_type)

        if start_date:
            query = query.filter(Transaction.created_at >= start_date)

        if end_date:
            query = query.filter(Transaction.created_at <= end_date)

        # Order by newest first
        query = query.order_by(Transaction.created_at.desc())

        # Get total count
        total = query.count()

        # Apply pagination
        offset = (page - 1) * per_page
        transactions = query.offset(offset).limit(per_page).all()

        # Format results
        transaction_list = []
        for txn in transactions:
            transaction_list.append({
                "transaction_id": txn.id,
                "from_account_id": txn.from_account_id,
                "to_account_id": txn.to_account_id,
                "amount": round(txn.amount, 2),
                "type": txn.transaction_type.value,
                "status": txn.status.value,
                "description": txn.description,
                "timestamp": txn.created_at.isoformat()
            })

        return {
            "account_id": account_id,
            "account_number": account.account_number,
            "transactions": transaction_list,
            "pagination": {
                "page": page,
                "per_page": per_page,
                "total": total,
                "total_pages": (total + per_page - 1) // per_page
            }
        }
