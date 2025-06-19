import math as m
import time
from power_subsystem import Power_Subsystem
class Spacecraft:
    def __init__(self, norad_id, name, orbital_altitude, orbital_period, mass, mission, country):

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
        self.mission = mission
        self.country = country

        #Attaching the power subsystem
        self.power_subsystem = Power_Subsystem()
    
    def get_battery_status(self):
        print(f"[Battery] Current Percentage: {self.power_system.get_battery_level():.2f}%")
    