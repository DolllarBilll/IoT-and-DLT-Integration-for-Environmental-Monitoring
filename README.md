# IoT and DLT Integration
## Environmental Monitoring System using MQTT, SQLite and Shimmer DLT

### Master’s Thesis

---

## Description

This application was developed as part of a Master’s thesis on the topic:

> **IoT and DLT Integration**

The goal of the project is to integrate **Internet of Things (IoT)** technologies with **Distributed Ledger Technologies (DLT)**, using the **Shimmer Network**, in order to ensure the integrity of the collected data.

The system simulates environmental sensors, collects data through MQTT, stores it in a local SQLite database, and creates a cryptographic fingerprint (SHA-256 Hash) for each measurement cycle. The Hash is published to the Shimmer Network, enabling data integrity verification.

---

# Technologies Used

- Python 3
- MQTT
- Eclipse Mosquitto Broker
- SQLite
- SHA-256
- Shimmer Network
- REST API
- Tkinter GUI

---

# Project Structure

```text
Project Master
│
├── launcher/
│     ├── launcher.py
│     ├── ui.py
│     ├── process_manager.py
│     ├── config.py
│     └── logger.py
│
├── sensors/
│     ├── temperature_sensor.py
│     ├── humidity_sensor.py
│     └── air_quality_sensor.py
│
├── mqtt/
│     └── publisher.py
│
├── gateway/
│     └── gateway.py
│
├── storage/
│     ├── database.py
│     ├── view_database.py
│     └── environmental_data.db
│
├── dlt/
│     ├── hashing.py
│     ├── shimmer_publish.py
│     └── verify_integrity.py
│
└── launcher.exe
```

---

# Operation Flow

```text
Sensors
    │
    ▼
MQTT Publisher
    │
    ▼
Mosquitto Broker
    │
    ▼
Gateway
    │
    ├────────► SQLite Database
    │
    ├────────► SHA-256 Hash
    │
    └────────► Shimmer Network
                  │
                  ▼
             Transaction ID
```

---

# Collected Data

For each cycle, the following are stored:

- Cycle ID
- Temperature
- Humidity
- Air Quality
- Timestamp
- SHA-256 Hash
- Shimmer Transaction ID

---

# Launcher

The Launcher serves as the central management point of the project.

### Available Functions

- Start Project
- Stop Project
- Create Database
- View Database
- Verify Integrity
- Open Project Folder
- Open Shimmer Explorer
- Exit

It also displays the status of:

- MQTT
- Gateway
- Publisher
- Database

---

# Data Integrity

For each cycle:

1. Measurements are collected.
2. A SHA-256 Hash is generated.
3. The Hash is published to the Shimmer Network.
4. The Transaction ID is stored.
5. Verify Integrity recalculates the Hash and compares the result.

Any modification to the stored data is detected immediately.

---

# Requirements

The following are required:

- Windows 10 or newer
- Python 3.x
- Eclipse Mosquitto Broker
- Internet Connection

---

# Execution

Simply run:

```text
launcher.exe
```

and use the graphical interface.

---

# Usage

1. Create Database
2. Start Project
3. Wait for measurements to be generated
4. View Database
5. Verify Integrity
6. Stop Project

---

# Educational Purpose

The application was developed exclusively for research and educational purposes as part of the Master’s thesis.

---

# Author

Vasileios Konstantinidis

Department of Computer Engineering and Electronics Systems

International Hellenic University (IHU)

---

# License

The project was created exclusively for academic use as part of a Master’s thesis.
