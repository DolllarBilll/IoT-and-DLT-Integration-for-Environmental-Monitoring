import random
from datetime import datetime, timezone


class HumiditySensor:
    def __init__(
        self,
        sensor_id="HUM_01",
        location="office_a",
        initial_humidity=50.0
    ):
        self.sensor_id = sensor_id
        self.sensor_type = "humidity"
        self.location = location
        self.unit = "%"

        self.humidity = initial_humidity

    def update_humidity(
        self,
        temperature_change=0.0
    ):

        random_change = random.choices(
            population=[0.0, 0.1, -0.1],
            weights=[70, 15, 15],
            k=1
        )[0]

        temperature_effect = -temperature_change

        self.humidity += (
            random_change +
            temperature_effect
        )

        self.humidity = max(
            30.0,
            min(80.0, self.humidity)
        )

    def get_status(self):

        if self.humidity < 35:
            return "warning"

        if self.humidity > 75:
            return "warning"

        return "normal"

    def generate_reading(
        self,
        temperature_change=0.0
    ):

        self.update_humidity(
            temperature_change
        )

        return {
            "sensor_id": self.sensor_id,
            "sensor_type": self.sensor_type,
            "location": self.location,
            "value": round(self.humidity, 1),
            "unit": self.unit,
            "status": self.get_status(),
            "timestamp": datetime.now(
                timezone.utc
            ).isoformat()
        }