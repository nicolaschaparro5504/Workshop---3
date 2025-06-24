# Modeling and Integration of Spacecraft Subsystems Using Object-Oriented Programming

## Overview

This project demonstrates the modeling and integration of key spacecraft subsystems using Python and object-oriented programming (OOP) principles. Each subsystem is encapsulated in its own class, allowing for modularity, reusability, and clear interfaces between components.

The main `Spacecraft` class coordinates the interaction between all subsystems, simulating realistic operations such as power management, altitude/orientation control, payload operation, anomaly detection, and communications.

---

## Subsystems

### 1. `Power_Subsystem`
- Manages the spacecraft's battery level and solar charging.
- Handles energy consumption for all actions and triggers solar charging when battery is low.
- Provides battery status to other subsystems.

### 2. `Communication_Subsystem`
- Simulates sending status messages and summaries.
- Consumes power for each message sent.
- Interfaces with the power subsystem to check battery before sending.

### 3. `Payload_Subsystem`
- Manages activation, deactivation, and operation of scientific payloads (e.g., SAR Radar, Cloud Seeding Device).
- Tracks energy consumption and runtime for each payload.
- Reports status and handles safe switching between payload types.

### 4. `Altitude_Control_Subsystem`
- Controls spacecraft altitude and orientation (pitch, roll, yaw).
- Consumes power for maneuvers and triggers charging cycles if battery is low.
- Reports current altitude and orientation.

### 5. `AnomalyDetectionSubsystem`
- Monitors the status of payloads and power system.
- Detects and reports anomalies, such as sensor malfunctions or eclipse events.

### 6. `Spacecraft`
- Integrates all subsystems.
- Provides high-level methods for changing altitude/orientation, managing payloads, simulating orbits, and reporting status.

---

## How to Run and Test

## Installation
Clone this repository and navigate into the project folder:
```bash
git clone https://github.com/nicolaschaparro5504/Workshop---3.git


### 1. Define the Spacecraft Object
Test_1=Spacecraf(norad_id, name, orbital_altitude, orbital_period, mass, country)

### 2. Activate Payload
Activates the payload subsystem with the specified payload type
        Sensor 1: SAR Radar
        Sensor 2: Cloud Seeding Device
        Sensor 3: Ionospheric Particle Collector
Test_1.activate_payload("SAR Radar")

### 3. Change the altitude and Orientation
Test_1.change_altitude(new_altitude) #Put the desired altitude
Test_1.change_orientation(x,y,z) #(pitch, roll, yaw) put the desired orientation

### 4. Update Payload
Test_1.update_payload_operation(dt) #dt is the desired duration

### 5. simulate orbit
Test_1.simulate_orbit()

### 6. send message
Test_1.send_message("working")

### 7. Check anomalies
Test_1.check_anomalies()

### 8. Handle eclipse
Test_1.handle_eclipse(is_sunlight_phase, is_charging)

### 9. Deactivate Payload
Test_1.deactivate_payload()

### 10. Get battery status
Test_1.get_battery_status()

### 11. Final Report
Test_1.report_status()

##  File Structure
spacecraft.py
power_subsystem.py
communication_subsystem.py
payload_subsystem.py
altitude_control_subsystem.py
anomaly_detection_subsystem.py

## Requirements
Python 3.7+
No external dependencies required

## Key OOP Concepts Used
Encapsulation: Each subsystem is a class with its own state and methods.
Inheritance: All subsystems inherit from a common Subsystem base class.
Composition: The Spacecraft class composes all subsystems.
Polymorphism: Subsystems can override base methods as needed.

## Authors
*   Diego Francesco Alessandroni Lince
*   Jonh Jairo Urriago Suarez
*   Nicolas Chaparro Barrantes

## Notes
The code is modular and can be extended with more subsystems or features.
For real-world applications, consider adding error handling, logging, and more detailed simulation logic.
