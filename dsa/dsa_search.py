"""
dsa_search.py
Task 5: Data Structures & Algorithms (DSA) Integration

Compares two ways of finding a MoMo SMS transaction by its "id",
using the REAL transactions parsed from the XML backup file:

1. LINEAR SEARCH : transactions stored as a plain Python list.
2. DICTIONARY LOOKUP: the same transactions stored as a dictionary
   (id -> transaction).

Both are timed over many repeated searches, and the results plus a
written reflection are printed and saved to a text file.
"""

import os
import time
import random

from xml_parser import parse_sms_xml

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REAL_XML_PATH = os.path.join(BASE_DIR, "modified_sms_v2.xml")
REPORT_PATH = os.path.join(BASE_DIR, "dsa_comparison_results.txt")

MIN_RECORDS = 20 


def load_transactions(xml_path=REAL_XML_PATH):
    """Parse the real XML file into a list of transaction dicts."""
    if not os.path.exists(xml_path):
        raise FileNotFoundError(
            f"Could not find the dataset at: {xml_path}\n"
            "Put modified_sms_v2.xml in the same folder as this script."
        )
    transactions = parse_sms_xml(xml_path)
    if len(transactions) < MIN_RECORDS:
        raise ValueError(
            f"Only {len(transactions)} records found; the assignment "
            f"needs at least {MIN_RECORDS}."
        )
    return transactions


def linear_search(transactions_list, target_id):
    """Check every item one by one. O(n). Returns the dict or None."""
    for transaction in transactions_list:
        if transaction["id"] == target_id:
            return transaction
    return None


def build_transaction_dict(transactions_list):
    """Convert the list into {id: transaction}."""
    return {transaction["id"]: transaction for transaction in transactions_list}


def dict_lookup(transactions_dict, target_id):
    """Hash-table lookup. O(1). Returns the dict or None."""
    return transactions_dict.get(target_id)


def compare_performance(transactions_list, transactions_dict, num_trials=10000):
    """Time num_trials searches with each method; return both durations."""
    max_id = max(t["id"] for t in transactions_list)

    ids_to_search = [random.randint(1, max_id) for _ in range(num_trials)]
    # Make ~5% of searches use ids that don't exist (linear search's worst case)
    for i in range(0, num_trials, 20):
        ids_to_search[i] = max_id + 1 + (i % 10)

    start = time.perf_counter()
    for target_id in ids_to_search:
        linear_search(transactions_list, target_id)
    linear_duration = time.perf_counter() - start

    start = time.perf_counter()
    for target_id in ids_to_search:
        dict_lookup(transactions_dict, target_id)
    dict_duration = time.perf_counter() - start

    return linear_duration, dict_duration


REFLECTION_TEXT = """
REFLECTION
----------

Q: Why is dictionary lookup faster than linear search?

A: A list has no idea where a specific id lives, so linear search
has to check items one at a time until it finds a match - in the
worst case it checks every single item. A dictionary works
differently: it uses a hash table, which turns the key (the id)
into a "hash" number and uses that number to jump almost directly
to the right memory slot. That means a dictionary lookup takes
roughly the same amount of time whether there are 20 transactions
or 20 million (this is called O(1), constant time), while linear
search gets slower as the list grows (this is called O(n), linear
time). The trade-off is that the dictionary uses extra memory and
must be built once up front.

Q: Can you suggest another data structure or algorithm that could
   improve search efficiency?

A: If we needed to search by something other than a unique id (for
example, "find all transactions between amount X and amount Y", or
"find the next transaction after a certain timestamp"), a
dictionary alone would not help, since it is only fast for exact-key
lookups. A better fit for range-based searches would be:

  - Binary Search on a sorted list: if we keep the transactions
    sorted by id (or by amount, or by date), binary search can find
    a record in O(log n) time by repeatedly cutting the search area
    in half. This is slower than a dictionary for exact-id lookups,
    but it naturally supports range queries that dictionaries can't.

  - A balanced tree structure like a B-Tree (which is what most real
    databases use internally for indexes): it keeps data sorted AND
    gives fast O(log n) lookups, so it's a nice middle ground between
    a plain list and a hash-based dictionary, especially for large,
    frequently-updated datasets like our MoMo transaction records.
"""


def build_report(transactions_list, linear_duration, dict_duration, num_trials):
    speedup = linear_duration / dict_duration if dict_duration > 0 else float("inf")

    report_lines = [
        "MoMo SMS API - DSA Comparison Report",
        "=====================================",
        "",
        f"Data source: {os.path.basename(REAL_XML_PATH)} (real parsed transactions)",
        f"Number of transactions searched over: {len(transactions_list)}",
        f"Number of searches timed per method:  {num_trials}",
        "",
        f"Linear Search total time:     {linear_duration:.6f} seconds",
        f"Dictionary Lookup total time: {dict_duration:.6f} seconds",
        f"Dictionary lookup was approximately {speedup:.1f}x faster than linear search.",
        "",
        REFLECTION_TEXT.strip(),
        "",
    ]
    return "\n".join(report_lines)


if __name__ == "__main__":
    random.seed(42)  # same search sequence every run
    NUM_TRIALS = 10000

    # 1. Load the real data
    transactions_list = load_transactions()
    print(f"Loaded {len(transactions_list)} REAL transactions from {REAL_XML_PATH}\n")

    transactions_dict = build_transaction_dict(transactions_list)

    # 2. Sanity check: both methods must agree on every id and on a missing id
    for t in transactions_list:
        assert linear_search(transactions_list, t["id"]) == dict_lookup(transactions_dict, t["id"])
    missing_id = len(transactions_list) + 1000
    assert linear_search(transactions_list, missing_id) is None
    assert dict_lookup(transactions_dict, missing_id) is None
    print("Sanity check passed: both methods agree on every transaction id "
          "(and both return None for a missing id).\n")

    # 3. Time both methods
    linear_duration, dict_duration = compare_performance(
        transactions_list, transactions_dict, num_trials=NUM_TRIALS
    )

    # 4. Build the report and print it
    report = build_report(transactions_list, linear_duration, dict_duration, NUM_TRIALS)
    print(report)

    # 5. Save it for the PDF report
    with open(REPORT_PATH, "w") as f:
        f.write(report)
    print(f"\nSaved full report to {REPORT_PATH}")
