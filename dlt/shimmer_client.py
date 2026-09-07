"""
IoT + DLT Integration Project

Shimmer Client
DLT Communication
"""

from iota_sdk import Client


class ShimmerClient:
    """
    Handles communication with the
    Shimmer distributed ledger.
    """
     
    def __init__(self):
        """
        Initializes the Shimmer client
        using the public Shimmer node.
        """

        self.client = Client(
            nodes=[
                "https://api.shimmer.network"
            ]
        )

    def connect(self):
        """
        Establishes a connection to the
        Shimmer network and checks
        the node status.
        """
         
        try:

            info = self.client.get_info()

            print("\n========== SHIMMER ==========")
            print("Connected successfully!")
            print(f"Network : {info.nodeInfo.protocol.networkName}")
            print(f"Healthy : {info.nodeInfo.status.isHealthy}")
            print("=============================\n")

            return True

        except Exception as e:

            print("\nShimmer connection failed!")
            print(e)

            return False

    def publish_hash(self, hash_value):
        """
        Publishes a SHA-256 hash to the
        Shimmer ledger using a Tagged Data block
        and returns the generated Block ID.
        """

        tag = "0x" + "ENVIRONMENTAL_DATA_HASH".encode().hex()
        data = "0x" + hash_value.encode().hex()

        block_id, _ = self.client.build_and_post_block(
            tag=tag,
            data=data
        )

        print("\n========== SHIMMER ==========")
        print("Hash published successfully!")
        print(f"Block ID : {block_id}")
        print("=============================\n")

        return block_id

    def get_block(self, block_id):

        return self.client.get_block_data(block_id)


_client = ShimmerClient()


def connect():

    return _client.connect()


def publish_hash(hash_value):

    return _client.publish_hash(hash_value)


def get_block(block_id):

    return _client.get_block(block_id)