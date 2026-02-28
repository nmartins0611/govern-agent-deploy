"""Integration tests for API routes"""

import pytest
import json


class TestHealthCheck:
    """Tests for health check endpoint"""

    def test_health_check(self, client):
        """Test health check endpoint"""
        response = client.get('/api/v1/health')

        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'healthy'
        assert data['service'] == 'banking-api'


class TestGetBalanceRoute:
    """Tests for balance endpoint"""

    def test_get_balance_success(self, client, session, sample_accounts):
        """Test getting balance via API"""
        response = client.get(f'/api/v1/accounts/{sample_accounts[0].id}/balance')

        assert response.status_code == 200
        data = response.get_json()
        assert data['account_id'] == sample_accounts[0].id
        assert data['balance'] == 1000.00

    def test_get_balance_not_found(self, client):
        """Test getting balance for non-existent account"""
        response = client.get('/api/v1/accounts/non-existent/balance')

        assert response.status_code == 404
        data = response.get_json()
        assert 'error' in data


class TestTransferRoute:
    """Tests for transfer endpoint"""

    def test_transfer_success(self, client, session, sample_accounts):
        """Test successful transfer via API"""
        payload = {
            'from_account_id': sample_accounts[0].id,
            'to_account_id': sample_accounts[1].id,
            'amount': 100.00,
            'description': 'API test transfer'
        }

        response = client.post(
            '/api/v1/accounts/transfer',
            data=json.dumps(payload),
            content_type='application/json'
        )

        assert response.status_code == 201
        data = response.get_json()
        assert data['amount'] == 100.00
        assert data['status'] == 'completed'

    def test_transfer_missing_fields(self, client):
        """Test transfer with missing required fields"""
        payload = {
            'from_account_id': 'test-id'
            # Missing to_account_id and amount
        }

        response = client.post(
            '/api/v1/accounts/transfer',
            data=json.dumps(payload),
            content_type='application/json'
        )

        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data

    def test_transfer_insufficient_funds(self, client, session, sample_accounts):
        """Test transfer with insufficient funds"""
        payload = {
            'from_account_id': sample_accounts[2].id,  # Has only 100.00
            'to_account_id': sample_accounts[0].id,
            'amount': 500.00
        }

        response = client.post(
            '/api/v1/accounts/transfer',
            data=json.dumps(payload),
            content_type='application/json'
        )

        assert response.status_code == 400
        data = response.get_json()
        assert 'Insufficient funds' in data['error']

    def test_transfer_invalid_amount(self, client, session, sample_accounts):
        """Test transfer with invalid amount"""
        payload = {
            'from_account_id': sample_accounts[0].id,
            'to_account_id': sample_accounts[1].id,
            'amount': -50.00
        }

        response = client.post(
            '/api/v1/accounts/transfer',
            data=json.dumps(payload),
            content_type='application/json'
        )

        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data

    def test_transfer_non_json_body(self, client):
        """Test transfer with non-JSON request body"""
        response = client.post(
            '/api/v1/accounts/transfer',
            data='not json',
            content_type='text/plain'
        )

        assert response.status_code == 400


class TestTransactionsRoute:
    """Tests for transactions endpoint"""

    def test_get_transactions_success(self, client, session, sample_accounts, sample_transactions):
        """Test getting transactions via API"""
        response = client.get(f'/api/v1/accounts/{sample_accounts[0].id}/transactions')

        assert response.status_code == 200
        data = response.get_json()
        assert 'transactions' in data
        assert 'pagination' in data
        assert data['pagination']['total'] == 2

    def test_get_transactions_with_pagination(self, client, session, sample_accounts, sample_transactions):
        """Test transaction pagination via API"""
        response = client.get(
            f'/api/v1/accounts/{sample_accounts[0].id}/transactions?page=1&per_page=1'
        )

        assert response.status_code == 200
        data = response.get_json()
        assert len(data['transactions']) == 1
        assert data['pagination']['per_page'] == 1

    def test_get_transactions_account_not_found(self, client):
        """Test getting transactions for non-existent account"""
        response = client.get('/api/v1/accounts/non-existent/transactions')

        assert response.status_code == 404
        data = response.get_json()
        assert 'error' in data


class TestRootEndpoint:
    """Tests for root endpoint"""

    def test_root_endpoint(self, client):
        """Test root endpoint returns API info"""
        response = client.get('/')

        assert response.status_code == 200
        data = response.get_json()
        assert data['service'] == 'Banking API'
        assert 'endpoints' in data
