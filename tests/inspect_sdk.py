from iota_sdk import Client

client = Client(
    nodes=["https://api.shimmer.network"]
)

print(client.build_and_post_block.__doc__)