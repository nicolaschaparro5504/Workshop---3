import math as m
import time
from power_subsystem import Power_Subsystem
from altitude_control_subsystem import Altitude_Control_Subsystem
from comms_subsystem import Communication_Subsystem
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

        #Altitude

        self.altitude_control = Altitude_Control_Subsystem(orbital_altitude)
        self.altitude_control.attach_power_system(self.power_subsystem)
        self.altitude_control.attach_comms(self.comms_subsystem)

        #Comms

        self.comms_subsystem.attach_power_system(self.power_subsystem)
        
        #Power
        self.power_subsystem.attach_comms(self.comms_subsystem)


    def get_battery_status(self):
        self.comms_subsystem.send_status(f"[Battery] Current Percentage: {self.power_subsystem.get_battery_level():.2f}%")

    def change_altitude(self, new_altitude):
        if 50 < new_altitude <= 2000: 
            self.altitude_control.update_altitude(new_altitude)
        else:
            self.comms_subsystem.send_status("[Altitude] Desired altitude is not possible")
    
    def change_orientation(self, x, y, z):
        self.altitude_control.update_orientation([x,y,z])

    def report_status(self):
        self.comms_subsystem.send_status(f"Spacecraft: {self.name} (NORAD ID: {self.norad_id})")
        self.altitude_control.report_ACS()
        self.get_battery_status()


sc = Spacecraft(1332, "LEO", 200, 2, 400, "USA")