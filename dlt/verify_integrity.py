"""
IoT + DLT Integration Project

Integrity Verification
SQLite and Shimmer Validation
"""

import os
import sys
import sqlite3

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from dlt.hashing import generate_hash
from dlt.shimmer_client import get_block


DB_NAME = "storage/environmental_data.db"


def decode_ledger_hash(block):
    """
    Extracts the SHA-256 hash stored inside
    the Shimmer Tagged Data payload.
    """

    payload = block.payload

    if payload is None:
        raise ValueError("Block has no payload.")

    data = payload.data

    if data.startswith("0x"):
        data = data[2:]

    return bytes.fromhex(data).decode("utf-8")


def verify_database():
    """
    Verifies the integrity of all stored
    environmental measurement cycles by
    comparing the recalculated SHA-256 hash
    with both the SQLite database and the
    corresponding Shimmer ledger entry.
    """

    connection = sqlite3.connect(DB_NAME)

    cursor = connection.cursor()

    # Retrieve all stored measurement cycles.
    cursor.execute(
        """
        SELECT

            cycle_id,
            timestamp,
            temperature,
            humidity,
            air_quality,
            hash,
            transaction_id

        FROM environment_data
        ORDER BY cycle_id
        """
    )

    rows = cursor.fetchall()

    connection.close()

    print()
    print("=" * 70)
    print("DATABASE + SHIMMER INTEGRITY VERIFICATION")
    print("=" * 70)

    verified = 0

    for row in rows:

        cycle = {

            "cycle_id": row[0],
            "timestamp": row[1],
            "temperature": row[2],
            "humidity": row[3],
            "air_quality": row[4]

        }

        stored_hash = row[5]
        transaction_id = row[6]

        calculated_hash = generate_hash(cycle)

        local_ok = calculated_hash == stored_hash

        ledger_ok = False
        ledger_hash = None

        try:

            if transaction_id:

                block = get_block(transaction_id)

                ledger_hash = decode_ledger_hash(block)

                ledger_ok = ledger_hash == calculated_hash

        except Exception as e:

            print(
                f"\nCycle {row[0]} "
                f"(Shimmer Error: {e})"
            )

        print()
        print("-" * 70)
        print(f"Cycle : {row[0]}")

        print()

        if local_ok:
            print("SQLite Verification : VERIFIED")
        else:
            print("SQLite Verification : TAMPERED")

        if transaction_id:

            if ledger_ok:
                print("Shimmer Verification: VERIFIED")
            else:
                print("Shimmer Verification: FAILED")

        else:
            print("Shimmer Verification: NO BLOCK ID")

        if local_ok and ledger_ok:

            print("\nOverall Status      : VERIFIED")
            verified += 1

        else:

            print("\nOverall Status      : FAILED")

    print()
    print("=" * 70)
    print(
        f"Verified Cycles : {verified}/{len(rows)}"
    )
    print("=" * 70)


if __name__ == "__main__":

    verify_database()

print("\nVerification completed.")
input("Press Enter to close...")