# IoT and DLT Integration
## Σύστημα Περιβαλλοντικής Παρακολούθησης με χρήση MQTT, SQLite και Shimmer DLT

### Διπλωματική Εργασία

---

## Περιγραφή

Η παρούσα εφαρμογή αναπτύχθηκε στο πλαίσιο διπλωματικής εργασίας με θέμα:

> **IoT and DLT Integration**

Στόχος του έργου είναι η ενοποίηση τεχνολογιών **Internet of Things (IoT)** με **Distributed Ledger Technologies (DLT)**, χρησιμοποιώντας το **Shimmer Network**, ώστε να διασφαλίζεται η ακεραιότητα των συλλεγόμενων δεδομένων.

Το σύστημα προσομοιώνει περιβαλλοντικούς αισθητήρες, συλλέγει δεδομένα μέσω MQTT, τα αποθηκεύει σε τοπική βάση SQLite και δημιουργεί κρυπτογραφικό αποτύπωμα (SHA-256 Hash) για κάθε κύκλο μετρήσεων. Το Hash δημοσιεύεται στο Shimmer Network, επιτρέποντας την επαλήθευση της ακεραιότητας των δεδομένων.

---

# Χρησιμοποιούμενες Τεχνολογίες

- Python 3
- MQTT
- Eclipse Mosquitto Broker
- SQLite
- SHA-256
- Shimmer Network
- REST API
- Tkinter GUI

---

# Δομή Έργου

```
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

# Ροή Λειτουργίας

```
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

# Δεδομένα που Συλλέγονται

Για κάθε κύκλο αποθηκεύονται:

- Cycle ID
- Temperature
- Humidity
- Air Quality
- Timestamp
- SHA-256 Hash
- Shimmer Transaction ID

---

# Launcher

Ο Launcher αποτελεί το κεντρικό σημείο διαχείρισης του έργου.

### Παρεχόμενες λειτουργίες

- Start Project
- Stop Project
- Create Database
- View Database
- Verify Integrity
- Open Project Folder
- Open Shimmer Explorer
- Exit

Επιπλέον εμφανίζει την κατάσταση των:

- MQTT
- Gateway
- Publisher
- Database

---

# Ακεραιότητα Δεδομένων

Για κάθε κύκλο:

1. Συλλέγονται οι μετρήσεις.
2. Δημιουργείται SHA-256 Hash.
3. Δημοσιεύεται το Hash στο Shimmer Network.
4. Αποθηκεύεται το Transaction ID.
5. Το Verify Integrity επανυπολογίζει το Hash και συγκρίνει το αποτέλεσμα.

Οποιαδήποτε αλλαγή στα αποθηκευμένα δεδομένα εντοπίζεται άμεσα.

---

# Προϋποθέσεις

Απαιτούνται:

- Windows 10 ή νεότερο
- Python 3.x
- Eclipse Mosquitto Broker
- Internet Connection

---

# Εκτέλεση

Απλά εκτελέστε:

```
launcher.exe
```

και χρησιμοποιήστε το γραφικό περιβάλλον.

---

# Χρήση

1. Create Database
2. Start Project
3. Περιμένετε να δημιουργηθούν μετρήσεις
4. View Database
5. Verify Integrity
6. Stop Project

---

# Εκπαιδευτικός Σκοπός

Η εφαρμογή δημιουργήθηκε αποκλειστικά για ερευνητικούς και εκπαιδευτικούς σκοπούς στο πλαίσιο της διπλωματικής εργασίας.

---

# Συγγραφέας

Βασίλειος Κωνσταντινίδης

Τμήμα Μηχανικών Πληροφορικής και Ηλεκτρονικών Συστημάτων

Διεθνές Πανεπιστήμιο Ελλάδος (IHU)

---

# Άδεια Χρήσης

Το έργο δημιουργήθηκε αποκλειστικά για ακαδημαϊκή χρήση στο πλαίσιο διπλωματικής εργασίας.