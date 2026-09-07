"""
IoT + DLT Integration Project

SHA-256 Hash Generation
Environmental Data Integrity
"""

import hashlib
import json


def generate_hash(cycle):
    """
    Generates a deterministic SHA-256 hash
    from a normalized environmental
    measurement cycle.
    """

    # Normalize the data to ensure
    # consistent hash generation.
    normalized_cycle = {

        "cycle_id":
            int(cycle["cycle_id"]),

        "timestamp":
            str(cycle["timestamp"]),

        "temperature":
            round(float(cycle["temperature"]), 2),

        "humidity":
            round(float(cycle["humidity"]), 2),

        "air_quality":
            int(cycle["air_quality"])
    }

    # Convert the normalized cycle into
    # a deterministic JSON string.
    cycle_string = json.dumps(
        normalized_cycle,
        sort_keys=True
    )

    # Generate the SHA-256 hash.
    cycle_hash = hashlib.sha256(
        cycle_string.encode()
    ).hexdigest()

    return cycle_hash