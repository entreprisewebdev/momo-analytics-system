"""
xml_parser.py
Task 1: Data Parsing


WHAT THIS FILE DOES
Reads the raw MoMo SMS backup file (modified_sms_v2.xml) and turns
every <sms> element into a clean Python dictionary with the fields
the assignment asks for: transaction type, amount, sender,
receiver, and timestamp (plus a few extras - fee, balance, and the
transaction reference number - that are useful for the API and the
dashboard too).

This file was built by looking at real examples of every message
type found in the dataset, so all 1691 records in the provided
file get classified (no message falls through to "other").
"""

import xml.etree.ElementTree as ET
import json
import re
import collections


# STEP 1: Figure out what kind of transaction a message is

# Order matters here - some checks have to come before others

def classify_type(body):
    """Return a short string describing what kind of SMS this is."""
    text = body.lower()

    if "one-time password" in text:
        return "otp"
    if "reversed" in text or "reversal" in text:
        return "reversal"
    if "failed at" in text:
        return "failed"
    if "you have received" in text:
        return "received"
    if "withdrawn" in text:
        return "withdrawal"
    if "you have transferred" in text:
        return "bank_transfer"
    if "transferred to" in text:
        return "transfer"
    if "umaze kugura" in text:
        return "bundle_purchase"
    if "transaction of" in text and " by " in text:
        return "merchant_payment"
    if "deposit" in text:
        return "deposit"
    if "airtime" in text:
        return "airtime"
    if "payment of" in text:
        return "payment"
    return "other"  # should not happen on the provided dataset, kept as a safety net

# STEP 2: Small helper for pulling a value out of the message text

def _extract(pattern, body, cast=str, flags=re.IGNORECASE):
    """
    Run `pattern` against `body` and return the first captured group,
    converted with `cast`. Returns None if there's no match, instead
    of crashing - real SMS text is messy and not every field is
    present in every message.
    """
    match = re.search(pattern, body, flags)
    if not match:
        return None
    value = match.group(1).strip()
    if cast is int:
        value = value.replace(",", "")
        return int(value) if value.isdigit() else None
    return value


def _amount(body):
    """The first 'X,XXX RWF' amount mentioned is the transaction amount
    in every message format in this dataset."""
    return _extract(r'([\d,]+)\s*RWF', body, cast=int)


def _fee(body):
    return _extract(r'Fee (?:was|paid)[:]?\s*([\d,]+)\s*RWF', body, cast=int)


def _balance(body):
    return _extract(r'(?:new balance|NEW BALANCE)\s*(?:is)?\s*:?\s*([\d,]+)\s*RWF', body, cast=int)


def _txn_ref(body):
    """The internal MTN MoMo transaction reference, when the message
    includes one (roughly half of messages do)."""
    return _extract(r'(?:TxId:?\s*|Financial Transaction Id:\s*)(\d+)', body, cast=str)


# STEP 3: Per-type field extraction
# Each function pulls out sender/receiver (as best as the text
# allows) for one specific message type. "self" means the account
# holder whose phone this backup came from.

def _fields_received(body):
    return {
        "sender": _extract(r'from (.+?)\s*\(', body),
        "receiver": "self",
    }


def _fields_payment(body):
    return {
        "sender": "self",
        "receiver": _extract(r'to ([A-Za-z\.\s]+?)\s+\d+\s+has been completed', body)
                    or _extract(r'to ([A-Za-z\.\s]+?)\s+with token', body)
                    or _extract(r'to ([A-Za-z\.\s]+?)\s+has been completed', body),
    }


def _fields_transfer(body):
    return {
        "sender": "self",
        "receiver": _extract(r'transferred to (.+?)\s*\(', body),
    }


def _fields_bank_transfer(body):
    return {
        "sender": "self",
        "receiver": _extract(r'transferred [\d,]+\s*RWF to (.+?)\s*\(', body),
    }


def _fields_deposit(body):
    return {
        "sender": "bank",
        "receiver": "self",
    }


def _fields_merchant_payment(body):
    return {
        "sender": "self",
        "receiver": _extract(r'by (.+?)\s+on your MOMO account', body),
    }


def _fields_airtime(body):
    return {
        "sender": "self",
        "receiver": "airtime",
    }


def _fields_withdrawal(body):
    return {
        "sender": "self",
        "receiver": _extract(r'via agent:\s*(.+?)\s*\(', body),
    }


def _fields_bundle_purchase(body):
    return {
        "sender": "self",
        "receiver": "bundle_purchase",
    }


def _fields_reversal(body):
    return {
        "sender": "self",
        "receiver": _extract(r'to (.+?)\s*\(', body),
    }


def _fields_failed(body):
    return {
        "sender": "self",
        "receiver": _extract(r'for (.+?)\s+with message', body),
    }


def _fields_otp(body):
    return {"sender": None, "receiver": None}


def _fields_other(body):
    return {"sender": None, "receiver": None}


# Dispatch table: look up the right extractor by transaction type
_FIELD_EXTRACTORS = {
    "received": _fields_received,
    "payment": _fields_payment,
    "transfer": _fields_transfer,
    "bank_transfer": _fields_bank_transfer,
    "deposit": _fields_deposit,
    "merchant_payment": _fields_merchant_payment,
    "airtime": _fields_airtime,
    "withdrawal": _fields_withdrawal,
    "bundle_purchase": _fields_bundle_purchase,
    "reversal": _fields_reversal,
    "failed": _fields_failed,
    "otp": _fields_otp,
    "other": _fields_other,
}

# STEP 4: Put it all together - one <sms> element -> one dictionary

def parse_sms_element(sms_element, transaction_id):
    """
    Convert one <sms> XML element into a transaction dictionary.

    `transaction_id` is our own sequential id (1, 2, 3, ...), used
    as the API's primary key. We assign it ourselves rather than
    relying on the MoMo transaction reference in the text, because
    that reference is missing from roughly half of all messages
    """
    body = sms_element.get("body") or ""
    txn_type = classify_type(body)

    record = {
        "id": transaction_id,
        "type": txn_type,
        "amount": _amount(body),
        "fee": _fee(body),
        "balance_after": _balance(body),
        "transaction_ref": _txn_ref(body),
        "timestamp": sms_element.get("readable_date"),
    }

    # Merge in the sender/receiver fields for this specific type
    record.update(_FIELD_EXTRACTORS[txn_type](body))

    return record


def parse_sms_xml(xml_path):
    """
    Parse the full XML backup file into a list of transaction
    dictionaries - this is the main entry point for the rest of
    the project (API, DSA search, dashboard, etc.).
    """
    tree = ET.parse(xml_path)
    root = tree.getroot()

    transactions = []
    for index, sms in enumerate(root, start=1):
        transactions.append(parse_sms_element(sms, transaction_id=index))

    return transactions

# STEP 5: Run directly to parse the file and save it as JSON

if __name__ == "__main__":
    INPUT_PATH = "modified_sms_v2.xml"
    OUTPUT_PATH = "sms_transactions.json"

    transactions = parse_sms_xml(INPUT_PATH)

    # Save as a proper JSON file - this is what the API, DSA search,
    # and dashboard code should all read from.
    with open(OUTPUT_PATH, "w") as f:
        json.dump(transactions, f, indent=2)

    # --- Summary, so we can sanity-check the parsing quality ---
    type_counts = collections.Counter(t["type"] for t in transactions)
    missing_amount = sum(1 for t in transactions if t["amount"] is None)
    missing_receiver = sum(
        1 for t in transactions if t["type"] not in ("otp", "other") and t["receiver"] is None
    )

    print(f"Parsed {len(transactions)} transactions -> {OUTPUT_PATH}\n")
    print("Breakdown by type:")
    for txn_type, count in type_counts.most_common():
        print(f"  {txn_type:<18} {count}")
    print(f"\nRecords with no amount found:   {missing_amount}")
    print(f"Records missing a receiver name: {missing_receiver}")

    print("\nSample record:")
    print(json.dumps(transactions[1], indent=2))  # a 'payment' example