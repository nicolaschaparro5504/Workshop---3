from power_subsystem import Power_Subsystem

class Altitude_Control_Subsystem:
    def __init__(self, altitude):
        self.orientation = [0, 0, 0] #Pitch, Roll, Yaw
        self.altitude = altitude
        self.power_system = None  # It will be connected from Spacecraft

    def attach_power_system(self, power_system):
        """Method to connect the power subsystem to the altitude system in order to consume battery when 
        performing an action
        """
        self.power_system = power_system
    
    def attach_comms(self, comm_system):
        """Allows the altitude subsystem to use the comms subsystem to send messages"""
        self.comm_system = comm_system

    def update_altitude(self, target_altitude):
        """Method to change altitude and consume power"""
        if self.power_system is None:
            self.comm_system.send_status("[Altitude Control] Power subsystem is not connected")
            return

        delta = abs(target_altitude - self.altitude)
        energy_needed = delta * 0.1  # 0.1 units of power per km changed

        self.comm_system.send_status(f"[Altitude] Manuvering from {self.altitude} km to {target_altitude} km, (Δ={delta} km)")
        self.comm_system.send_status(f"[Altitude] Battery needed: {energy_needed:.2f}%")

        if self.power_system.consume_energy(energy_needed): # Calls the power subsystem to consume energy
            self.altitude = target_altitude
            self.comm_system.send_status(f"[Altitude] Maneuver completed. New altitud: {self.altitude} km")
        else:
            self.comm_system.send_status("[Altitude] Maneuver canceled, there's not enough battery")

        self.comm_system.send_status(f"[Power] Battery Level: {self.power_system.get_battery_level():.2f} %")

        if self.power_system.get_battery_level() < 30: # Calls the power subsytem if the battery is low to start solar charge
            self.comm_system.send_status("[Power] Charging...")
            minuto = 1
            while self.power_system.battery_level < 80:
                self.comm_system.send_status(f"[Time] → Minute {minuto}")
                self.power_system.update_power(1)  # 1 minute simulated
                minuto += 1


    def update_orientation(self, target_orientation):
        if self.power_system is None:
            self.comm_system.send_status("[Orientation] Power subsystem is not connected")
            return

        delta_degrees = sum(abs(a - b) for a, b in zip(self.orientation, target_orientation))
        energy_needed = (delta_degrees / 10.0) * 1.0  # 1% per 10° of degree change

        """zip combines the values of each axis in pairs a and b and calculates the difference between them
        then sums the difference between the three axis and divides it by ten
        """

        self.comm_system.send_status(f"[Orientation] Orienting from: {self.orientation} to {target_orientation}")
        self.comm_system.send_status(f"[Orientation] Battery required: {energy_needed:.2f}%")

        if self.power_system.consume_energy(energy_needed):
            self.orientation = target_orientation
            self.comm_system.send_status(f"[Orientation] Orientation completed. New orientation: {self.orientation}")
        else:
            self.comm_system.send_status(f"[Orientation] There's not enough battery to change the orientation")

        self.comm_system.send_status(f"[Power] Battery Level: {self.power_system.get_battery_level():.2f} %")

        if self.power_system.get_battery_level() < 30:
            self.comm_system.send_status("[Power] Charging...")
            minuto = 1
            while self.power_system.battery_level < 80:
                self.comm_system.send_status(f"[Time] → Minute {minuto}")
                self.power_system.update_power(1)
                minuto += 1

    def report_ACS(self):
        self.comm_system.send_status(f"[Altitude] Current altitude: {self.altitude} km")
        self.comm_system.send_status(f"[Orientation] Current orientation: {self.orientation}")
        