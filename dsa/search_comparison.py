import json
import time
from pathlib import Path


# Load transactions from the JSON file
DATA_FILE = Path(__file__).parent.parent / "data" / "transactions.json"

with open(DATA_FILE, "r", encoding="utf-8") as file:
    transactions = json.load(file)


# Linear Search
def linear_search(transactions, target_id):
    for transaction in transactions:
        if transaction["id"] == target_id:
            return transaction

    return None


# Dictionary Lookup
transaction_dict = {
    transaction["id"]: transaction
    for transaction in transactions
}


def dictionary_lookup(transaction_dict, target_id):
    return transaction_dict.get(target_id)


# Use at least 20 records for the comparison
test_records = transactions[:20]


# Measure Linear Search
linear_start = time.perf_counter()

for transaction in test_records:
    linear_search(transactions, transaction["id"])

linear_end = time.perf_counter()


# Measure Dictionary Lookup
dictionary_start = time.perf_counter()

for transaction in test_records:
    dictionary_lookup(transaction_dict, transaction["id"])

dictionary_end = time.perf_counter()


linear_time = linear_end - linear_start
dictionary_time = dictionary_end - dictionary_start


print("DSA Search Comparison")
print("--------------------")
print(f"Total transactions: {len(transactions)}")
print(f"Test records: {len(test_records)}")
print()
print(f"Linear Search time:     {linear_time:.10f} seconds")
print(f"Dictionary Lookup time: {dictionary_time:.10f} seconds")
print()
print("Time Complexity:")
print("Linear Search: O(n)")
print("Dictionary Lookup: O(1) average case")