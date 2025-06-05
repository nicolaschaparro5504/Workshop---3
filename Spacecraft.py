import math as m

class Spacecraft:
    def __init__(self, norad_id, name, orbital_altitude, orbital_period, mass, mission, country, region):

        """
        Definition of basic parameters of an spacecraft

        Arguments:

        name: name of the spacecraft
        norad_id: number of identification of the spacecraft
        orbital_altitude(km): altitude of operation
        orbital_period(hours): time that takes to complete an orbit
        mass(kg): initial mass of the spacecraft with full fuel
        country: country that deployed the spacecraft
        region: region in which the spacecraft works

        """
        self.norad_id = norad_id
        self.name = name
        self.orbital_altitude = orbital_altitude
        self.orbital_period = orbital_period
        self.mass = mass
        self.mission = mission
        self.country = country
        self.region = region