"""
IoT + DLT Integration Project

Launcher Configuration
"""

import sys
from pathlib import Path


# Project root directory
if getattr(sys, "frozen", False):
    # Εκτέλεση από launcher.exe
    PROJECT_ROOT = Path(sys.executable).resolve().parent
else:
    # Εκτέλεση από Python
    PROJECT_ROOT = Path(__file__).resolve().parent.parent


# Project folders
GATEWAY_DIR = PROJECT_ROOT / "gateway"
MQTT_DIR = PROJECT_ROOT / "mqtt"
DLT_DIR = PROJECT_ROOT / "dlt"
STORAGE_DIR = PROJECT_ROOT / "storage"
VIEW_DATABASE_SCRIPT = PROJECT_ROOT / "storage" / "view_database.py"


# Python scripts
GATEWAY_SCRIPT = GATEWAY_DIR / "gateway.py"

PUBLISHER_SCRIPT = MQTT_DIR / "publisher.py"

VERIFY_SCRIPT = DLT_DIR / "verify_integrity.py"

DATABASE_SCRIPT = STORAGE_DIR / "database.py"

DATABASE_FILE = STORAGE_DIR / "environmental_data.db"


# External programs
MOSQUITTO_COMMAND = "mosquitto -v"


# Shimmer Explorer
SHIMMER_EXPLORER = "https://explorer.shimmer.network/shimmer"


# Window titles
WINDOW_MOSQUITTO = "Mosquitto Broker"

WINDOW_GATEWAY = "Gateway"

WINDOW_PUBLISHER = "Publisher"

WINDOW_VERIFY = "Integrity Verification"


# Refresh interval (milliseconds)
STATUS_REFRESH = 1000


# Application title
APPLICATION_TITLE = (
    "IoT + DLT Integration Project - Environmental Monitoring System"
)