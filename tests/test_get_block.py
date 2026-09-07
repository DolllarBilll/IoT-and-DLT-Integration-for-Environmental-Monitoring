import os
import sys

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from dlt.shimmer_client import get_block

block_id = input("Block ID: ")

block = get_block(block_id)

print(type(block))
print(type(block.payload))

print("\nPAYLOAD")
print(block.payload)

print("\nTAG")
print(block.payload.tag)

print("\nDATA")
print(block.payload.data)