class Power_Subsystem:
    def __init__(self):
        self.battery_level = 100.0
        self.solar_charging = False
        self.consumption_rate = 0.5   # Consuption per minute
        self.charge_rate = 0.1        # Charge per minute

    def update_power(self, dt):
        """Method to update the power over time, general consumption of the spacecraft"""
    # Only consume if not charging
        if not self.solar_charging:
            consumption = self.consumption_rate * dt
            self.battery_level -= consumption
            self.battery_level = max(self.battery_level, 0)
            print(f"[Power] Consumption: -{consumption:.2f}%, Remaining battery: {self.battery_level:.2f}%")

    #Activates solar charging when battery is less than 30%
        if self.battery_level < 30 and not self.solar_charging:
            self.solar_charging = True
            print("[Power] Low battery: Initializing solar charging")

    # Recharges the battery if solar charging is activated
        if self.solar_charging:
            self.recharge(dt)

    def recharge(self, dt):
        charge = self.charge_rate * dt
        self.battery_level += charge
        if self.battery_level >= 95:
            self.battery_level = 95
            self.solar_charging = False
            print("[Power] Battery at 95% capacity. Stopping solar charging")
        else:
            print(f"[Power] Charging: +{charge:.2f}%, Battery Level: {self.battery_level:.2f}%")

    def consume_energy(self, amount):
        """Method to update the power wherever an action is performed"""
        if self.battery_level >= amount:
            self.battery_level -= amount
            print(f"[Power] Action Consumption: -{amount:.2f}%, Battery Level: {self.battery_level:.2f}%")

            if self.battery_level < 30 and not self.solar_charging:
                self.solar_charging = True
                print("[Power] Low battery: Initializing solar charging")
            return True
        return False

    def get_battery_level(self):
        """Method to check the battery level at any time"""
        return self.battery_level
