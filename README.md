# MoMo Analytics System

A Python-based MoMo Analytics System that processes mobile money SMS records and provides a REST API for securely managing transaction data.

## Project Overview

The MoMo Analytics System processes SMS records from a mobile money service. The system parses the provided XML dataset, converts the records into structured transaction data, provides search functionality, and exposes the transaction data through a REST API.

The project demonstrates:

* XML data parsing
* JSON data processing
* REST API development
* CRUD operations
* Basic Authentication
* Data Structures and Algorithms
* API testing and validation
* API documentation

## Project Structure

```text
momo-analytics-system/
│
├── api/
│   ├── __init__.py
│   ├── app.py
│   ├── db.py
│   ├── schemas.py
│   └── server.py
│
├── dsa/
│   ├── dsa_search.py
│   ├── dsa_comparison_results.txt
│   ├── modified_sms_v2.xml
│   ├── sms_transactions.json
│   └── xml_parser.py
│
├── data/
│   └── transactions.json
│
├── docs/
│   ├── api_docs.md
│   ├── Database Design Document (1).pdf
│   └── ERD.jpeg
│
├── screenshots/
│   ├── 01_get_authenticated.png
│   ├── 02_get_unauthorized.png
│   ├── 03_post_success.png
│   ├── 04_put_success.png
│   └── 05_delete_success.png
│
├── database/
│   └── database_setup.sql
│
├── tests/
│
├── web/
│
├── scripts/
│
├── requirements.txt
└── README.md
```

## Requirements

Before running the project, make sure you have:

* Python 3
* Git
* A terminal
* `curl` for API testing

A virtual environment is recommended.

## Setup

Clone the repository:

```bash
git clone https://github.com/entreprisewebdev/momo-analytics-system.git
cd momo-analytics-system
```

Create a virtual environment:

```bash
python3 -m venv .venv
```

Activate it on macOS/Linux:

```bash
source .venv/bin/activate
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Data

The project uses the `modified_sms_v2.xml` dataset containing mobile money SMS records.

The dataset contains information such as:

* Transaction ID
* Transaction type
* Amount
* Timestamp
* Sender/receiver information
* Transaction message

The XML records are processed and converted into structured JSON transaction objects.

## REST API

The REST API is implemented in plain Python using the built-in `http.server` module.

### Starting the API

From the project root, run:

```bash
python3 api/server.py
```

The API runs locally at:

```text
http://localhost:8000
```

## Authentication

The API uses Basic Authentication to protect its endpoints.

For testing, the credentials are:

```text
Username: admin
Password: password
```

Example:

```bash
curl -u admin:password http://localhost:8000/transactions
```

Requests without valid credentials receive a `401 Unauthorized` response.

Example:

```bash
curl http://localhost:8000/transactions
```

Response:

```json
{
  "error": "Unauthorized",
  "message": "Valid username and password are required."
}
```

### Security Note

Basic Authentication is suitable for demonstrating authentication in this assignment, but it is not ideal for a production system. The credentials are Base64 encoded rather than encrypted, so HTTPS should be used to protect them during transmission.

Stronger authentication approaches such as JWT or OAuth 2.0 can be considered for production systems.

## API Endpoints

### GET /transactions

Returns all transactions.

```bash
curl -u admin:password http://localhost:8000/transactions
```

Example response:

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

### GET /transactions/{id}

Returns a single transaction.

```bash
curl -u admin:password \
http://localhost:8000/transactions/76662021700
```

### POST /transactions

Creates a new transaction.

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

### PUT /transactions/{id}

Updates an existing transaction.

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

### DELETE /transactions/{id}

Deletes an existing transaction.

```bash
curl -u admin:password \
-X DELETE http://localhost:8000/transactions/TEST-001
```

Example response:

```json
{
  "message": "Transaction deleted successfully"
}
```

## HTTP Status Codes

| Status Code | Meaning                            |
| ----------- | ---------------------------------- |
| `200`       | Request completed successfully     |
| `201`       | Transaction created successfully   |
| `400`       | Bad request or invalid JSON        |
| `401`       | Authentication required or invalid |
| `404`       | Transaction or endpoint not found  |
| `409`       | Transaction already exists         |

## Data Structures and Algorithms

The project compares two approaches for searching transaction records by ID:

### Linear Search

Linear search scans the transaction list one record at a time until the required ID is found.

**Time complexity:**

```text
O(n)
```

### Dictionary Lookup

Transactions can also be stored in a Python dictionary using the transaction ID as the key.

**Average time complexity:**

```text
O(1)
```

### Comparison Results

The DSA comparison was performed using the transaction dataset.

```text
Total transactions: 1691
Searches per method: 10000

Linear Search:       0.896232 seconds
Dictionary Lookup:   0.002017 seconds
```

The dictionary lookup was approximately **444.2 times faster** in the recorded comparison.

Dictionary lookup is faster because it uses a hash table, allowing the program to access a value directly through its key rather than scanning the records one by one.

Other data structures or algorithms, such as balanced search trees or indexed databases, could also improve search efficiency depending on the requirements of the system.

## Testing and Validation

The API was tested using `curl`.

The tests covered:

* Successful authenticated GET request
* Unauthorized request
* Successful POST request
* Successful PUT request
* Successful DELETE request

### Screenshots

The test screenshots are available in the `screenshots/` directory:

```text
screenshots/
├── 01_get_authenticated.png
├── 02_get_unauthorized.png
├── 03_post_success.png
├── 04_put_success.png
└── 05_delete_success.png
```

The CRUD lifecycle was also tested by creating a test transaction, retrieving it, updating it, deleting it, and confirming that it could no longer be retrieved.

## API Documentation

Detailed API documentation is available in:

```text
docs/api_docs.md
```

The documentation contains:

* Endpoint and method
* Authentication requirements
* Request examples
* Response examples
* Error codes
* Security considerations

## Team Collaboration

The project was completed collaboratively, with each team member responsible for specific technical tasks.

### Malaika — Tasks 2 & 3

**API Implementation and Authentication & Security**

* Implemented the REST API using Python's built-in `http.server`.
* Implemented CRUD endpoints:

  * `GET /transactions`
  * `GET /transactions/{id}`
  * `POST /transactions`
  * `PUT /transactions/{id}`
  * `DELETE /transactions/{id}`
* Implemented Basic Authentication for protected API endpoints.
* Implemented authentication error handling for unauthorized requests.
* Tested authenticated and unauthorized API requests.
* Implemented JSON request and response handling.

### Erica — Tasks 1 & 5

**Data Parsing and DSA Integration**

* Parsed the `modified_sms_v2.xml` dataset.
* Converted SMS records into JSON transaction objects.
* Implemented Linear Search for transaction records.
* Implemented Dictionary Lookup for transaction records.
* Compared the efficiency of the two search approaches.
* Recorded the search performance results.

### Sam — Tasks 4 & 6

**API Documentation and Testing & Validation**

* Prepared the API endpoint documentation.
* Documented request and response examples.
* Documented API error codes.
* Conducted API testing using `curl`.
* Captured screenshots showing successful and unauthorized requests.
* Verified CRUD operations and authentication behavior.

## Team Coordination

The team used GitHub to collaborate and integrate the individual technical contributions into the final MoMo Analytics System.

Each team member was responsible for their assigned technical tasks, and the completed work was integrated into the shared repository.

## Conclusion

The MoMo Analytics System provides a REST API for securely accessing and managing mobile money transaction data. The project demonstrates XML data processing, CRUD API development, authentication, data structure comparison, and API testing.

The implementation also demonstrates the performance advantage of dictionary-based lookup over linear search for transaction ID searches while highlighting the security limitations of Basic Authentication and the potential use of stronger authentication mechanisms in production systems.