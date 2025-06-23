class Payload_Subsystem:
    def __init__(self, payload_type: str = "SAR Radar"):
        """
        Initialize the payload subsystem.
        :param payload_type: Type of payload (default: "SAR Radar")
        """
        self.active: bool = False
        self.payload_type: str = payload_type
        self.power_subsystem = None
        self.comms_subsystem = None
        self.operating_in_earth_shadow: bool = False  # Simulates eclipse periods in LEO

        # Energy consumption per minute (% battery/min)
        self.payload_consumption = {
            "SAR Radar": 1.5,
            "Cloud Seeding Device": 2.0,
            "Ionospheric Particle Collector": 1.0
        }

        # Total active time (in minutes)
        self.total_runtime: float = 0.0

    def attach_power(self, power_subsystem) -> None:
        """Connects to the power subsystem."""
        self.power_subsystem = power_subsystem

    def attach_comms(self, comms_subsystem) -> None:
        """Connects to the communication subsystem."""
        self.comms_subsystem = comms_subsystem

    def activate_payload(self) -> None:
        """Activates the payload if enough power is available."""
        if not self.power_subsystem or not self.comms_subsystem:
            raise Exception("Subsystems not connected.")

        if self.active:
            return  # Already active

        if self.power_subsystem.consume_energy(0.5, log=False):
            self.active = True
            battery = self.power_subsystem.get_battery_level()
            self.comms_subsystem.send_status(
                f"[Payload] {self.payload_type} activated in LEO orbit. Battery: {battery:.3f}%",
                skip_summary=False
            )
        else:
            self.comms_subsystem.send_status(
                f"[Payload] Activation failed: Not enough power for {self.payload_type}.",
                skip_summary=False
            )

    def deactivate_payload(self) -> None:
        """Deactivates the payload."""
        if not self.comms_subsystem:
            raise Exception("Communication subsystem not connected.")
        if self.active:
            self.active = False
            self.reset()
            battery = self.power_subsystem.get_battery_level()
            self.comms_subsystem.send_status(
                f"[Payload] {self.payload_type} deactivated. Battery: {battery:.3f}%",
                skip_summary=True
            )

    def update_operation(self, dt: float, in_earth_shadow: bool = False) -> None:
        """
        Updates the payload operation over a time interval (dt in minutes),
        taking into account whether the satellite is in Earth's shadow.
        """
        if not self.power_subsystem or not self.comms_subsystem:
            raise Exception("Subsystems not connected.")

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

    def get_status(self) -> dict:
        """Returns current status of the payload and optionally sends a summary."""
        status_info = {
            "Payload Type": self.payload_type,
            "Active": self.active,
            "Total Runtime (min)": self.total_runtime,
            "In Earth's Shadow": self.operating_in_earth_shadow
    }
        summary = ", ".join(f"{key}: {value}" for key, value in status_info.items())
        self.comms_subsystem.send_status(f"[Payload Status] {summary}", skip_summary=True)

        return status_info


    def reset(self) -> None:
        """Resets the payload subsystem to initial state."""
        self.active = False
        self.total_runtime = 0.0
        self.operating_in_earth_shadow = False

    def set_payload_type(self, payload_type: str) -> None:
        """Safely change the payload type if supported."""
        if payload_type not in self.payload_consumption:
            raise ValueError(f"Unsupported payload type: {payload_type}")
        self.payload_type = payload_type
        self.reset()

