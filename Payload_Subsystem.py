class Payload_Subsystem:
    def __init__(self, payload_type="SAR Radar"):
        self.active = False
        self.payload_type = payload_type
        self.power_subsystem = None
        self.comms_subsystem = None
        self.operating_in_earth_shadow = False  # Simulates eclipse periods in LEO

        # Energy consumption per minute (% battery/min)
        self.payload_consumption = {
            "SAR Radar": 1.5,
            "Cloud Seeding Device": 2.0,
            "Ionospheric Particle Collector": 1.0
        }

        # Total active time (in minutes)
        self.total_runtime = 0.0

    def attach_power(self, power_subsystem):
        """Connects to the power subsystem"""
        self.power_subsystem = power_subsystem

    def attach_comms(self, comms_subsystem):
        """Connects to the communication subsystem"""
        self.comms_subsystem = comms_subsystem

    def activate_payload(self):
        """Activates the payload if enough power is available"""
        if not self.power_subsystem or not self.comms_subsystem:
            raise Exception("Subsystems not connected.")

        if self.active:
            return  # Already active

        if self.power_subsystem.consume_energy(0.5, log=False):
            self.active = True
            self.comms_subsystem.send_status(
                f"[Payload] {self.payload_type} activated in LEO orbit.",
                skip_summary=False
            )
        else:
            self.comms_subsystem.send_status(
                f"[Payload] Activation failed: Not enough power for {self.payload_type}.",
                skip_summary=False
            )

    def deactivate_payload(self):
        """Deactivates the payload"""
        if self.active:
            self.active = False
            self.comms_subsystem.send_status(
                f"[Payload] {self.payload_type} deactivated.",
                skip_summary=False
            )

    def update_operation(self, dt, in_earth_shadow=False):
        """
        Updates the payload operation over a time interval (dt in minutes),
        taking into account whether the satellite is in Earth's shadow.
        """
        self.operating_in_earth_shadow = in_earth_shadow

        if self.active:
            rate = self.payload_consumption.get(self.payload_type, 1.2)
            energy_needed = rate * dt
            success = self.power_subsystem.consume_energy(energy_needed)

            if success:
                self.total_runtime += dt
                visibility = "in Earth's shadow" if in_earth_shadow else "in sunlight"
                self.comms_subsystem.send_status(
                    f"[Payload] {self.payload_type} operating ({visibility}): -{energy_needed:.2f}%, Battery: {self.power_subsystem.get_battery_level():.2f}%",
                    skip_summary=True
                )
            else:
                self.comms_subsystem.send_status(
                    f"[Payload] {self.payload_type} stopped: Insufficient power.",
                    skip_summary=False
                )
                self.active = False

    def get_status(self):
        """Returns current status of the payload"""
        return {
            "payload": self.payload_type,
            "active": self.active,
            "total_runtime_min": self.total_runtime,
            "in_earth_shadow": self.operating_in_earth_shadow
        }
Payload_Cubesat = Payload_Subsystem("Cloud Seeding Device")

