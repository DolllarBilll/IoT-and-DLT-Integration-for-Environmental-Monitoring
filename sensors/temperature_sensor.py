import random
from datetime import datetime, timezone


class TemperatureSensor:
    def __init__(
        self,
        sensor_id="TEMP_01",
        location="office_a",
        initial_temperature=24.0
    ):
        self.sensor_id = sensor_id
        self.sensor_type = "temperature"
        self.location = location
        self.unit = "C"

        self.temperature = initial_temperature
        self.last_change = 0.0

    def update_temperature(self):

        change = random.choices(
            population=[0.0, 0.1, -0.1],
            weights=[70, 15, 15],
            k=1
        )[0]

        self.temperature += change

        self.temperature = max(
            18.0,
            min(30.0, self.temperature)
        )

        self.last_change = change

    def get_status(self):

        if self.temperature > 30:
            return "critical"

        if self.temperature >= 28:
            return "warning"

        return "normal"

    def generate_reading(self):

        self.update_temperature()

        return {
            "sensor_id": self.sensor_id,
            "sensor_type": self.sensor_type,
            "location": self.location,
            "value": round(self.temperature, 1),
            "unit": self.unit,
            "status": self.get_status(),
            "timestamp": datetime.now(
                timezone.utc
            ).isoformat()
        }

    def get_last_change(self):
        return self.last_change