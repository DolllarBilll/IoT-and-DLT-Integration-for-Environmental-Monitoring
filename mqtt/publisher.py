"""
IoT + DLT Integration Project

MQTT Publisher
Simulated Environmental Sensors
"""

import os
import sys


PROJECT_ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        ".."
    )
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import json
import time

import paho.mqtt.client as mqtt

from sensors.temperature_sensor import (
    TemperatureSensor
)

from sensors.humidity_sensor import (
    HumiditySensor
)

from sensors.air_quality_sensor import (
    AirQualitySensor
)


BROKER = "localhost"
PORT = 1883


TOPICS = {
    "temperature": "environment/temperature",
    "humidity": "environment/humidity",
    "air_quality": "environment/airquality"
}


client = mqtt.Client()

client.connect(BROKER, PORT, 60)

# Initialize the simulated sensors.
temp_sensor = TemperatureSensor()

humidity_sensor = HumiditySensor()

aq_sensor = AirQualitySensor()


print("Publisher started...")

# Continuously generate and publish
# environmental sensor readings.
while True:

    # Generate a new set of sensor readings.
    temp_reading = (
        temp_sensor.generate_reading()
    )

    humidity_reading = (
        humidity_sensor.generate_reading(
            temperature_change=
            temp_sensor.get_last_change()
        )
    )

    aq_reading = (
        aq_sensor.generate_reading(
            temperature=temp_reading["value"],
            humidity=humidity_reading["value"]
        )
    )

    # Publish the sensor readings
    # to their corresponding MQTT topics.
    client.publish(
        TOPICS["temperature"],
        json.dumps(temp_reading)
    )

    client.publish(
        TOPICS["humidity"],
        json.dumps(humidity_reading)
    )

    client.publish(
        TOPICS["air_quality"],
        json.dumps(aq_reading)
    )

    print("Published:")
    print(temp_reading)
    print(humidity_reading)
    print(aq_reading)
    print("-" * 50)

    # Wait one minute before
    # generating the next cycle.
    time.sleep(60)