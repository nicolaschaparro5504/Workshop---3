import math as m
import time
from power_subsystem import Power_Subsystem
from altitude_control_subsystem import Altitude_Control_Subsystem
from comms_subsystem import Communication_Subsystem
from annomaly_detection_subsystem import AnomalyDetectionSubsystem
from Payload_Subsystem import Payload_Subsystem
class Spacecraft:
    def __init__(self, norad_id, name, orbital_altitude, orbital_period, mass, country):

        """
        Definition of basic parameters of an spacecraft

        Arguments:

        name: name of the spacecraft
        norad_id: number of identification of the spacecraft
        orbital_altitude(km): altitude of operation meassured from the surface of Earth
        orbital_period(hours): time that takes to complete an orbit
        mass(kg): initial mass of the spacecraft with full fuel
        country: country that deployed the spacecraft
        """
        self.norad_id = norad_id
        self.name = name
        self.orbital_altitude = orbital_altitude
        self.orbital_period = orbital_period
        self.mass = mass
        self.country = country

        #Attaching the subsystems
        self.power_subsystem = Power_Subsystem()
        self.comms_subsystem = Communication_Subsystem()
        self.payload_subsystem = Payload_Subsystem()

        self.anomaly_detection = AnomalyDetectionSubsystem(self.comms_subsystem, self.power_subsystem, self.payload_subsystem)
        
        
        #Altitude

        self.altitude_control = Altitude_Control_Subsystem(orbital_altitude)
        self.altitude_control.attach_power_system(self.power_subsystem)
        self.altitude_control.attach_comms(self.comms_subsystem)

        #Comms

        self.comms_subsystem.attach_power_system(self.power_subsystem)
        
        #Power
        self.power_subsystem.attach_comms(self.comms_subsystem)

        #Payload
        self.payload_subsystem.attach_power(self.power_subsystem)
        self.payload_subsystem.attach_comms(self.comms_subsystem)

    def get_battery_status(self):
        self.comms_subsystem.send_status(
            f"[Battery] Current Percentage: {self.power_subsystem.get_battery_level():.3f}%", 
            skip_summary=True)

    def change_altitude(self, new_altitude):
        if 50 < new_altitude <= 2000: 
            self.altitude_control.update_altitude(new_altitude)
        else:
            self.comms_subsystem.send_status("[Altitude] Desired altitude is not possible")
    
    def change_orientation(self, x, y, z):
        self.altitude_control.update_orientation([x,y,z])

    def send_message(self, message):
        self.comms_subsystem.send_status(message)
        # Mostrar batería restante después de enviar el mensaje
        self.comms_subsystem.send_status(
            f"[Battery] Remaining: {self.power_subsystem.get_battery_level():.3f}%",
        skip_summary=True)

    def report_status(self):
        self.comms_subsystem.send_status(f"Spacecraft: {self.name} (NORAD ID: {self.norad_id})")
        self.altitude_control.report_ACS()
        self.get_battery_status()

    def simulate_orbit(self):
        """
        Simulates the orbital period of the spacecraft, consuming energy for each minute of the orbit
        """
        total_minutes = int(self.orbital_period * 60)
        self.comms_subsystem.send_status(f"[Orbit] Starting orbit simulation for {total_minutes} minutes.")
        for minute in range(1, total_minutes + 1):
            # Simula consumo por sistemas básicos (ajusta el valor según tu modelo)
            self.power_subsystem.consume_energy(0.2, log=False)
            if minute % 60 == 0 or minute == total_minutes:
                self.comms_subsystem.send_status(
                    f"[Orbit] Minute {minute}: Remaining battery: {self.power_subsystem.get_battery_level():.2f}%",
                    skip_summary=True
                )
        self.comms_subsystem.send_status("[Orbit] Orbit simulation completed.")

    def activate_payload(self, payload_type):
        """
        Activates the payload subsystem with the specified payload type
        Sensor 1: SAR Radar
        Sensor 2: Cloud Seeding Device
        Sensor 3: Ionospheric Particle Collector

        """
        self.payload_subsystem.set_payload_type(payload_type)
        self.payload_subsystem.activate_payload()

    def update_payload_operation(self, dt, in_earth_shadow=False):
        """
        Updates the payload operation based on the time interval and whether the spacecraft is in Earth's shadow
        """
        self.payload_subsystem.update_operation(dt, in_earth_shadow)
        self.payload_subsystem.get_status()

    def deactivate_payload(self):
        """
        Deactivates the payload subsystem
        """
        self.payload_subsystem.deactivate_payload()
        
    def check_anomalies(self):
        """
        Checks for anomalies in the payload and power subsystems
        """
        self.anomaly_detection.check_active_payload()

    def handle_eclipse(self, is_sunlight_phase, is_charging):
        self.anomaly_detection.handle_eclipse(is_sunlight_phase, is_charging)

sc = Spacecraft(1332, "LEO", 200, 2, 400, "USA")