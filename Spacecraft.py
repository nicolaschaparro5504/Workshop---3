import math as m
import time
from power_subsystem import Power_Subsystem
from altitude_control_subsystem import Altitude_Control_Subsystem
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

        #Attaching the power subsystem
        self.power_subsystem = Power_Subsystem()

        self.altitude_control = Altitude_Control_Subsystem(orbital_altitude)
        self.altitude_control.attach_power_system(self.power_subsystem)


    def get_battery_status(self):
        print(f"[Battery] Current Percentage: {self.power_subsystem.get_battery_level():.2f}%")

    def change_altitude(self, new_altitude):
        if new_altitude > 50:
            self.altitude_control.update_altitude(new_altitude)
        else:
            print("[Altitude] Desired altitude is not possible")
    
    def change_orientation(self, x, y, z):
        self.altitude_control.update_orientation([x,y,z])

    def report_status(self):
        self.altitude_control.report_ACS()
        self.get_battery_status()


sc = Spacecraft(1332, "LEO", 200, 2, 400, "USA")