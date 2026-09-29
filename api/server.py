import json
import base64
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler


# Location of the transaction data
DATA_FILE = Path(__file__).parent.parent / "data" / "transactions.json"

# Basic Authentication credentials
USERNAME = "admin"
PASSWORD = "password"


def load_transactions():
    """Load transactions from the JSON file."""
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_transactions(transactions):
    """Save transactions to the JSON file."""
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(transactions, file, indent=2, ensure_ascii=False)


class TransactionAPI(BaseHTTPRequestHandler):

    def send_json(self, status_code, data):
        """Send a JSON response."""
        response = json.dumps(data, indent=2).encode("utf-8")

        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(response)))
        self.end_headers()

        self.wfile.write(response)

    def authenticate(self):
        """Check Basic Authentication credentials."""
        auth_header = self.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Basic "):
            return False

        try:
            encoded_credentials = auth_header.split(" ", 1)[1]

            decoded_credentials = base64.b64decode(
                encoded_credentials
            ).decode("utf-8")

            username, password = decoded_credentials.split(":", 1)

            return username == USERNAME and password == PASSWORD

        except (ValueError, UnicodeDecodeError):
            return False

    def unauthorized(self):
        """Return a 401 Unauthorized response."""
        self.send_response(401)
        self.send_header("Content-Type", "application/json")
        self.send_header(
            "WWW-Authenticate",
            'Basic realm="Transaction API"'
        )
        self.end_headers()

        response = json.dumps({
            "error": "Unauthorized",
            "message": "Valid username and password are required."
        }).encode("utf-8")

        self.wfile.write(response)

    def get_transaction_by_id(self, transaction_id):
        """Find a transaction by ID."""
        transactions = load_transactions()

        for transaction in transactions:
            if transaction["id"] == transaction_id:
                return transaction

        return None

    def read_request_body(self):
        """Read and parse JSON request data."""
        content_length = self.headers.get("Content-Length")

        if not content_length:
            return None

        try:
            length = int(content_length)
            body = self.rfile.read(length)
            return json.loads(body.decode("utf-8"))

        except (ValueError, json.JSONDecodeError):
            return None

    def do_GET(self):
        """Handle GET requests."""

        if not self.authenticate():
            self.unauthorized()
            return

        transactions = load_transactions()

        # GET /transactions
        if self.path == "/transactions":
            self.send_json(200, {
                "count": len(transactions),
                "transactions": transactions
            })
            return

        # GET /transactions/{id}
        if self.path.startswith("/transactions/"):
            transaction_id = self.path.split("/")[-1]

            for transaction in transactions:
                if transaction["id"] == transaction_id:
                    self.send_json(200, transaction)
                    return

            self.send_json(404, {
                "error": "Transaction not found"
            })
            return

        self.send_json(404, {
            "error": "Endpoint not found"
        })

    def do_POST(self):
        """Handle POST /transactions."""

        if not self.authenticate():
            self.unauthorized()
            return

        if self.path != "/transactions":
            self.send_json(404, {
                "error": "Endpoint not found"
            })
            return

        new_transaction = self.read_request_body()

        if new_transaction is None:
            self.send_json(400, {
                "error": "Invalid JSON request body"
            })
            return

        if "id" not in new_transaction:
            self.send_json(400, {
                "error": "Transaction ID is required"
            })
            return

        transactions = load_transactions()

        # Prevent duplicate IDs
        for transaction in transactions:
            if transaction["id"] == str(new_transaction["id"]):
                self.send_json(409, {
                    "error": "Transaction with this ID already exists"
                })
                return

        new_transaction["id"] = str(new_transaction["id"])
        transactions.append(new_transaction)

        save_transactions(transactions)

        self.send_json(201, new_transaction)

    def do_PUT(self):
        """Handle PUT /transactions/{id}."""

        if not self.authenticate():
            self.unauthorized()
            return

        if not self.path.startswith("/transactions/"):
            self.send_json(404, {
                "error": "Endpoint not found"
            })
            return

        transaction_id = self.path.split("/")[-1]
        updated_transaction = self.read_request_body()

        if updated_transaction is None:
            self.send_json(400, {
                "error": "Invalid JSON request body"
            })
            return

        transactions = load_transactions()

        for index, transaction in enumerate(transactions):
            if transaction["id"] == transaction_id:

                # Keep the original ID
                updated_transaction["id"] = transaction_id

                transactions[index] = updated_transaction

                save_transactions(transactions)

                self.send_json(200, updated_transaction)
                return

        self.send_json(404, {
            "error": "Transaction not found"
        })

    def do_DELETE(self):
        """Handle DELETE /transactions/{id}."""

        if not self.authenticate():
            self.unauthorized()
            return

        if not self.path.startswith("/transactions/"):
            self.send_json(404, {
                "error": "Endpoint not found"
            })
            return

        transaction_id = self.path.split("/")[-1]
        transactions = load_transactions()

        for index, transaction in enumerate(transactions):
            if transaction["id"] == transaction_id:

                deleted_transaction = transactions.pop(index)

                save_transactions(transactions)

                self.send_json(200, {
                    "message": "Transaction deleted successfully",
                    "transaction": deleted_transaction
                })
                return

        self.send_json(404, {
            "error": "Transaction not found"
        })


def run_server():
    """Start the API server."""

    server_address = ("localhost", 8000)

    server = HTTPServer(server_address, TransactionAPI)

    print("MoMo Transaction API running on http://localhost:8000")
    print("Press CTRL+C to stop the server.")

    server.serve_forever()


if __name__ == "__main__":
    run_server()