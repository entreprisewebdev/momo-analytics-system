import xml.etree.ElementTree as ET
import json
import re
from pathlib import Path


# File locations
XML_FILE = Path(__file__).parent.parent / "data" / "modified_sms_v2-1.xml"
JSON_FILE = Path(__file__).parent.parent / "data" / "transactions.json"


def get_transaction_id(body):
    """Extract a transaction ID from the SMS body."""
    patterns = [
        r"TxId:\s*(\d+)",
        r"Financial Transaction Id:\s*(\d+)",
        r"Financial Transaction ID:\s*(\d+)",
    ]

    for pattern in patterns:
        match = re.search(pattern, body, re.IGNORECASE)
        if match:
            return match.group(1)

    return None


def get_amount(body):
    """Extract the first RWF amount from the SMS body."""
    match = re.search(r"([\d,]+)\s*RWF", body, re.IGNORECASE)

    if match:
        return int(match.group(1).replace(",", ""))

    return None


def get_transaction_type(body):
    """Identify the transaction type from the SMS body."""
    text = body.lower()

    if "one-time password" in text:
        return "otp"

    if "bank deposit" in text or "cash deposit" in text:
        return "deposit"

    if "withdrawn" in text:
        return "withdrawal"

    if "transferred" in text:
        return "transfer"

    if "payment" in text:
        return "payment"

    if "received" in text:
        return "received"

    return "other"


def parse_sms():
    """Parse the XML file and return transactions as dictionaries."""
    tree = ET.parse(XML_FILE)
    root = tree.getroot()

    transactions = []

    for index, sms in enumerate(root.findall("sms"), start=1):
        body = sms.get("body", "")

        transaction_id = get_transaction_id(body)

        # Some SMS messages do not contain a transaction ID.
        # Give those records a unique ID for API operations.
        record_id = transaction_id or f"SMS-{index:04d}"

        transaction = {
            "id": record_id,
            "transaction_id": transaction_id,
            "transaction_type": get_transaction_type(body),
            "amount_rwf": get_amount(body),
            "timestamp": sms.get("readable_date"),
            "address": sms.get("address"),
            "body": body
        }

        transactions.append(transaction)

    return transactions


def save_to_json(transactions):
    """Save parsed transactions to a JSON file."""
    with open(JSON_FILE, "w", encoding="utf-8") as file:
        json.dump(transactions, file, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    transactions = parse_sms()
    save_to_json(transactions)

    print(f"Parsed SMS records: {len(transactions)}")
    print(f"JSON file created: {JSON_FILE}")