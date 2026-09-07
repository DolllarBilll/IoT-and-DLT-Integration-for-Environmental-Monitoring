import random
from datetime import datetime, timezone


class AirQualitySensor:
    def __init__(
        self,
        sensor_id="AQ_01",
        location="office_a",
        initial_aqi=60.0
    ):
        self.sensor_id = sensor_id
        self.sensor_type = "air_quality"
        self.location = location
        self.unit = "AQI"

        self.aqi = initial_aqi

    def update_aqi(
        self,
        temperature,
        humidity
    ):

        random_change = random.choices(
            population=[0.0, 1.0, -1.0],
            weights=[70, 15, 15],
            k=1
        )[0]

        environmental_effect = 0

        if temperature > 26:
            environmental_effect += 1

        if humidity < 40:
            environmental_effect += 1

        self.aqi += (
            random_change +
            environmental_effect
        )

        self.aqi = max(
            0,
            min(500, self.aqi)
        )

    def get_status(self):

        if self.aqi > 150:
            return "critical"

        if self.aqi > 100:
            return "warning"

        return "normal"

    def generate_reading(
        self,
        temperature,
        humidity
    ):

        self.update_aqi(
            temperature,
            humidity
        )

        return {
            "sensor_id": self.sensor_id,
            "sensor_type": self.sensor_type,
            "location": self.location,
            "value": round(self.aqi, 0),
            "unit": self.unit,
            "status": self.get_status(),
            "timestamp": datetime.now(
                timezone.utc
            ).isoformat()
        }