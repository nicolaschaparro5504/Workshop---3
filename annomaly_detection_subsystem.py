from subsystems_base import Subsystem

class AnomalyDetectionSubsystem (Subsystem):
    def __init__(self, comms_subsystem, power_subsystem, payload_subsystem):
        self.comms = comms_subsystem
        self.power = power_subsystem
        self.payload = payload_subsystem

    def check_active_payload(self):
    
        """
        Checks the currently active payload and sends status message.
        """
        payload_type = self.payload.payload_type
        is_active = self.payload.active

        if not is_active:
            self.comms.send_status(
            f"[ALERT] {payload_type} malfunction detected! Payload inactive."
        )
        else:
            self.comms.send_status(
            f"[STATUS] {payload_type} functioning normally. Payload is active."
        )

    def handle_eclipse(self, is_sunlight_phase, is_charging):
        """
        Detects eclipse or solar panel malfunction.
        If the spacecraft is in sunlight phase but not charging, switch to battery and send alert.
        """
        if is_sunlight_phase and not is_charging:
            self.comms.send_status("[ECLIPSE/MALFUNCTION] No power charging detected during sunlight phase. Possible eclipse or solar panel malfunction. Switching to battery power.")
            self.power.switch_to_battery()
        elif is_sunlight_phase and is_charging:
            self.comms.send_status("[POWER] Solar panels charging as expected during sunlight phase.")
            self.power.switch_to_solar()
        else:
            self.comms.send_status("[ECLIPSE] Spacecraft is in eclipse (no sunlight). Switching to battery power.")
            self.power.switch_to_battery()
