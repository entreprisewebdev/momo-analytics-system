# MoMo Transaction REST API Documentation

## 1. API Overview

The MoMo Transaction REST API provides authenticated access to mobile money transaction records. The API supports CRUD operations, allowing authorized clients to create, read, update, and delete transaction records.

The API was implemented in plain Python using the built-in `http.server` module.

**Base URL:**

```text
http://localhost:8000
```

## 2. Authentication

All API endpoints require HTTP Basic Authentication.

**Username:**

```text
admin
```

**Password:**

```text
password
```

Example:

```bash
curl -u admin:password http://localhost:8000/transactions
```

Requests without valid credentials receive:

```text
401 Unauthorized
```

## 3. GET /transactions

Returns all transaction records.

### Request

```bash
curl -u admin:password http://localhost:8000/transactions
```

### Response

```json
{
  "count": 1691,
  "transactions": [
    {
      "id": "76662021700",
      "transaction_id": "76662021700",
      "transaction_type": "received",
      "amount_rwf": 2000,
      "timestamp": "10 May 2024 4:30:58 PM",
      "address": "M-Money",
      "body": "..."
    }
  ]
}
```

### Status Codes

* `200 OK` — Transactions returned successfully.
* `401 Unauthorized` — Authentication is missing or invalid.
* `404 Not Found` — Endpoint does not exist.

---

## 4. GET /transactions/{id}

Returns one transaction using its ID.

### Request

```bash
curl -u admin:password \
http://localhost:8000/transactions/76662021700
```

### Response

```json
{
  "id": "76662021700",
  "transaction_id": "76662021700",
  "transaction_type": "received",
  "amount_rwf": 2000,
  "timestamp": "10 May 2024 4:30:58 PM",
  "address": "M-Money",
  "body": "..."
}
```

### Status Codes

* `200 OK` — Transaction found.
* `401 Unauthorized` — Authentication is missing or invalid.
* `404 Not Found` — Transaction does not exist.

---

## 5. POST /transactions

Creates a new transaction.

### Request

```bash
curl -u admin:password \
-X POST http://localhost:8000/transactions \
-H "Content-Type: application/json" \
-d '{
  "id": "TEST-001",
  "transaction_id": "TEST-001",
  "transaction_type": "payment",
  "amount_rwf": 5000,
  "timestamp": "29 September 2026 8:00:00 PM",
  "address": "M-Money",
  "body": "Test transaction created through the REST API"
}'
```

### Response

```json
{
  "id": "TEST-001",
  "transaction_id": "TEST-001",
  "transaction_type": "payment",
  "amount_rwf": 5000,
  "timestamp": "29 September 2026 8:00:00 PM",
  "address": "M-Money",
  "body": "Test transaction created through the REST API"
}
```

### Status Codes

* `201 Created` — Transaction created successfully.
* `400 Bad Request` — Invalid JSON or missing transaction ID.
* `401 Unauthorized` — Authentication is missing or invalid.
* `404 Not Found` — Endpoint does not exist.
* `409 Conflict` — Transaction ID already exists.

---

## 6. PUT /transactions/{id}

Updates an existing transaction.

### Request

```bash
curl -u admin:password \
-X PUT http://localhost:8000/transactions/TEST-001 \
-H "Content-Type: application/json" \
-d '{
  "transaction_id": "TEST-001",
  "transaction_type": "payment",
  "amount_rwf": 7500,
  "timestamp": "29 September 2026 8:00:00 PM",
  "address": "M-Money",
  "body": "Test transaction updated through the REST API"
}'
```

### Response

```json
{
  "transaction_id": "TEST-001",
  "transaction_type": "payment",
  "amount_rwf": 7500,
  "timestamp": "29 September 2026 8:00:00 PM",
  "address": "M-Money",
  "body": "Test transaction updated through the REST API",
  "id": "TEST-001"
}
```

### Status Codes

* `200 OK` — Transaction updated successfully.
* `400 Bad Request` — Invalid JSON.
* `401 Unauthorized` — Authentication is missing or invalid.
* `404 Not Found` — Transaction does not exist.

---

## 7. DELETE /transactions/{id}

Deletes an existing transaction.

### Request

```bash
curl -u admin:password \
-X DELETE http://localhost:8000/transactions/TEST-001
```

### Response

```json
{
  "message": "Transaction deleted successfully",
  "transaction": {
    "id": "TEST-001"
  }
}
```

### Status Codes

* `200 OK` — Transaction deleted successfully.
* `401 Unauthorized` — Authentication is missing or invalid.
* `404 Not Found` — Transaction does not exist.

---

## 8. Authentication Error Example

A request without credentials:

```bash
curl http://localhost:8000/transactions
```

returns:

```json
{
  "error": "Unauthorized",
  "message": "Valid username and password are required."
}
```

The API therefore prevents unauthenticated clients from accessing the transaction endpoints.

## 9. API Error Summary

| Status Code | Meaning                            |
| ----------- | ---------------------------------- |
| `200`       | Request completed successfully     |
| `201`       | Resource created successfully      |
| `400`       | Invalid request or JSON            |
| `401`       | Authentication required or invalid |
| `404`       | Resource or endpoint not found     |
| `409`       | Resource already exists            |

## 10. Security Considerations

The API uses Basic Authentication as required by the assignment. Basic Authentication is relatively weak because the username and password are encoded using Base64 rather than encrypted. Base64 encoding can be decoded, so Basic Authentication should be used with HTTPS to protect credentials while they are transmitted.

For a production system, stronger authentication mechanisms could be considered.

### JWT

JSON Web Tokens (JWT) allow an authenticated client to receive a signed token and use that token when making subsequent API requests. This avoids repeatedly sending the username and password with every request.

### OAuth 2.0

OAuth 2.0 provides a framework for delegated authorization. It is useful when applications need controlled access to resources without directly sharing a user's password with every application.

Therefore, while Basic Authentication meets the requirements of this assignment, JWT or OAuth 2.0 would be more appropriate for a production API depending on the system's authentication and authorization requirements.
