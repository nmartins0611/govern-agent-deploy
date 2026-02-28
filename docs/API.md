# Banking API Documentation

## Overview

The Banking API provides RESTful endpoints for basic banking operations including balance inquiries, fund transfers, and transaction history.

**Base URL:** `http://localhost:5000/api/v1`

**Version:** 1.0.0

## Authentication

Currently, the API does not require authentication. This is suitable for demo purposes only.

For production use, implement proper authentication (JWT, OAuth2, etc.).

## Endpoints

### Health Check

Check if the API is running and healthy.

**Endpoint:** `GET /api/v1/health`

**Response:**
```json
{
  "status": "healthy",
  "service": "banking-api",
  "version": "1.0.0"
}
```

**Example:**
```bash
curl http://localhost:5000/api/v1/health
```

---

### Get Account Balance

Retrieve the current balance for a specific account.

**Endpoint:** `GET /api/v1/accounts/<account_id>/balance`

**Parameters:**
- `account_id` (path): The unique account identifier

**Response (200 OK):**
```json
{
  "account_id": "test-account-1",
  "account_number": "TEST001",
  "holder_name": "Test User 1",
  "balance": 1000.00,
  "currency": "USD",
  "timestamp": "2026-02-28T10:30:00.000000"
}
```

**Error Responses:**
- `404 Not Found`: Account does not exist
- `400 Bad Request`: Invalid account ID format

**Example:**
```bash
curl http://localhost:5000/api/v1/accounts/test-account-1/balance
```

---

### Transfer Funds

Transfer money from one account to another.

**Endpoint:** `POST /api/v1/accounts/transfer`

**Request Body:**
```json
{
  "from_account_id": "test-account-1",
  "to_account_id": "test-account-2",
  "amount": 100.00,
  "description": "Payment for services"
}
```

**Fields:**
- `from_account_id` (required): Source account identifier
- `to_account_id` (required): Destination account identifier
- `amount` (required): Transfer amount (positive number, max 2 decimals)
- `description` (optional): Transaction description

**Response (201 Created):**
```json
{
  "transaction_id": "abc-123-def",
  "from_account": "TEST001",
  "to_account": "TEST002",
  "amount": 100.00,
  "status": "completed",
  "description": "Payment for services",
  "timestamp": "2026-02-28T10:35:00.000000"
}
```

**Error Responses:**
- `400 Bad Request`:
  - Missing required fields
  - Invalid amount (negative, zero, or too many decimals)
  - Insufficient funds
- `404 Not Found`: Source or destination account does not exist

**Example:**
```bash
curl -X POST http://localhost:5000/api/v1/accounts/transfer \
  -H "Content-Type: application/json" \
  -d '{
    "from_account_id": "test-account-1",
    "to_account_id": "test-account-2",
    "amount": 100.00,
    "description": "Payment for services"
  }'
```

---

### Get Transaction History

Retrieve paginated transaction history for an account.

**Endpoint:** `GET /api/v1/accounts/<account_id>/transactions`

**Parameters:**
- `account_id` (path): Account identifier
- `page` (query, optional): Page number (default: 1)
- `per_page` (query, optional): Items per page (default: 10, max: 100)
- `type` (query, optional): Filter by transaction type

**Response (200 OK):**
```json
{
  "account_id": "test-account-1",
  "account_number": "TEST001",
  "transactions": [
    {
      "transaction_id": "abc-123-def",
      "from_account_id": "test-account-1",
      "to_account_id": "test-account-2",
      "amount": 100.00,
      "type": "transfer",
      "status": "completed",
      "description": "Payment for services",
      "timestamp": "2026-02-28T10:35:00.000000"
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 10,
    "total": 25,
    "total_pages": 3
  }
}
```

**Error Responses:**
- `404 Not Found`: Account does not exist
- `400 Bad Request`: Invalid account ID format

**Example:**
```bash
# Get first page
curl http://localhost:5000/api/v1/accounts/test-account-1/transactions

# Get second page with 5 items per page
curl http://localhost:5000/api/v1/accounts/test-account-1/transactions?page=2&per_page=5
```

---

## Error Response Format

All error responses follow this format:

```json
{
  "error": "Description of the error"
}
```

## HTTP Status Codes

- `200 OK`: Request successful
- `201 Created`: Resource created successfully
- `400 Bad Request`: Invalid request data
- `404 Not Found`: Resource not found
- `405 Method Not Allowed`: HTTP method not supported
- `500 Internal Server Error`: Server error

## Rate Limiting

No rate limiting is currently implemented. For production, consider implementing rate limiting per IP or API key.

## CORS

CORS is enabled for all origins in development mode. Configure appropriately for production.
