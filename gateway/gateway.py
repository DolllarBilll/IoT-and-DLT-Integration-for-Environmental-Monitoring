"""
IoT + DLT Integration Project

MQTT Gateway
Data Collection, Hash Generation,
and Shimmer DLT Integration
"""

import os
import sys

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import json

import paho.mqtt.client as mqtt

from storage.database import (
    initialize_database,
    insert_cycle,
    get_last_cycle_id
)

from dlt.hashing import (
    generate_hash
)

from dlt.shimmer_client import (
    publish_hash
)


BROKER = "localhost"
PORT = 1883

TOPIC = "environment/#"


latest_data = {
    "temperature": None,
    "humidity": None,
    "air_quality": None,
    "timestamp": None
}


cycle_counter = get_last_cycle_id()


def create_cycle():
    """
    Creates a complete environmental measurement cycle
    from the latest sensor readings.
    """
    global cycle_counter

    cycle_counter += 1

    return {

        "cycle_id":
            cycle_counter,

        "temperature":
            latest_data["temperature"],

        "humidity":
            latest_data["humidity"],

        "air_quality":
            latest_data["air_quality"],

        "timestamp":
            latest_data["timestamp"]
    }


def on_connect(
    client,
    userdata,
    flags,
    reason_code,
    properties=None
):

    print("Connected to broker")

    client.subscribe(TOPIC)

    # Notify launcher that Gateway is ready
    client.publish(
        "gateway/status",
        "READY",
        qos=1
    )


def on_message(
    client,
    userdata,
    msg
):

    payload = json.loads(
        msg.payload.decode()
    )

    topic = msg.topic

    latest_data["timestamp"] = (
        payload["timestamp"]
    )

    if topic == "environment/temperature":

        latest_data["temperature"] = (
            payload["value"]
        )

    elif topic == "environment/humidity":

        latest_data["humidity"] = (
            payload["value"]
        )

    elif topic == "environment/airquality":

        latest_data["air_quality"] = (
            payload["value"]
        )

    # Create a cycle only when all sensors
    # have provided a new measurement.
    if (

        latest_data["temperature"] is not None
        and

        latest_data["humidity"] is not None
        and

        latest_data["air_quality"] is not None

    ):

        cycle = create_cycle()
        # Generate a SHA-256 hash for the completed cycle.
        cycle_hash = generate_hash(
            cycle
        )

        cycle["hash"] = cycle_hash
        # Publish the hash to the Shimmer network.
        transaction_id = publish_hash(
            cycle_hash
        )

        cycle["transaction_id"] = (
            transaction_id
        )
        # Store the completed cycle together with
        # its hash and Shimmer Block ID.
        insert_cycle(cycle)

        print(
            f"Cycle {cycle['cycle_id']} stored."
        )

        print(
            f"DLT Transaction: "
            f"{transaction_id}"
        )

        latest_data["temperature"] = None
        latest_data["humidity"] = None
        latest_data["air_quality"] = None
        latest_data["timestamp"] = None


initialize_database()


client = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION2
)

client.on_connect = on_connect

client.on_message = on_message

client.connect(
    BROKER,
    PORT,
    60
)

print("Gateway started...")

client.loop_forever()