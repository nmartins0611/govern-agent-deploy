"""API routes for the banking application"""

from flask import Blueprint, request, jsonify
from banking_app.services import BankingService
from banking_app.exceptions import (
    BankingError,
    AccountNotFoundError,
    InsufficientFundsError,
    InvalidAmountError,
    InvalidAccountError
)

api = Blueprint('api', __name__, url_prefix='/api/v1')


def get_service():
    """Get banking service instance with current session"""
    from flask import current_app
    return BankingService(current_app.db_session)


@api.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "banking-api",
        "version": "1.0.0"
    }), 200


@api.route('/accounts/<account_id>/balance', methods=['GET'])
def get_balance(account_id):
    """
    Get account balance

    Returns:
        JSON response with account balance
    """
    try:
        service = get_service()
        result = service.get_balance(account_id)
        return jsonify(result), 200

    except AccountNotFoundError as e:
        return jsonify({"error": str(e)}), 404

    except InvalidAccountError as e:
        return jsonify({"error": str(e)}), 400

    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500


@api.route('/accounts/transfer', methods=['POST'])
def transfer_funds():
    """
    Transfer funds between accounts

    Request body:
        {
            "from_account_id": "uuid",
            "to_account_id": "uuid",
            "amount": 100.50,
            "description": "Payment for services"
        }

    Returns:
        JSON response with transaction details
    """
    try:
        data = request.get_json(force=False, silent=True)

        if data is None:
            return jsonify({"error": "Request body must be JSON"}), 400

        from_account_id = data.get('from_account_id')
        to_account_id = data.get('to_account_id')
        amount = data.get('amount')
        description = data.get('description')

        if not from_account_id or not to_account_id or amount is None:
            return jsonify({
                "error": "Missing required fields: from_account_id, to_account_id, amount"
            }), 400

        service = get_service()
        result = service.transfer_funds(
            from_account_id=from_account_id,
            to_account_id=to_account_id,
            amount=amount,
            description=description
        )

        return jsonify(result), 201

    except AccountNotFoundError as e:
        return jsonify({"error": str(e)}), 404

    except InsufficientFundsError as e:
        return jsonify({"error": str(e)}), 400

    except InvalidAmountError as e:
        return jsonify({"error": str(e)}), 400

    except InvalidAccountError as e:
        return jsonify({"error": str(e)}), 400

    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500


@api.route('/accounts/<account_id>/transactions', methods=['GET'])
def get_transactions(account_id):
    """
    Get transaction history for an account

    Query parameters:
        - page: Page number (default: 1)
        - per_page: Items per page (default: 10, max: 100)
        - type: Filter by transaction type (optional)

    Returns:
        JSON response with paginated transaction history
    """
    try:
        page = request.args.get('page', 1)
        per_page = request.args.get('per_page', 10)
        transaction_type = request.args.get('type')

        service = get_service()
        result = service.get_transaction_history(
            account_id=account_id,
            page=page,
            per_page=per_page,
            transaction_type=transaction_type
        )

        return jsonify(result), 200

    except AccountNotFoundError as e:
        return jsonify({"error": str(e)}), 404

    except InvalidAccountError as e:
        return jsonify({"error": str(e)}), 400

    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500


@api.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({"error": "Endpoint not found"}), 404


@api.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 errors"""
    return jsonify({"error": "Method not allowed"}), 405
