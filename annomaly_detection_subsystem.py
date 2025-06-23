class AnomalyDetectionSubsystem:
    def __init__(self, comms_subsystem, power_subsystem):
        self.comms = comms_subsystem
        self.power = power_subsystem

    def check_sensors(self, SAR_Radar_status, Cloud_Seeding_Device_status, Ionospheric_Particle_Collector_status):
        # Simulate sensor checks (replace with real sensor logic)
        if not SAR_Radar_status:
            self.comms.send_status("[ALERT #01] SAR Radar malfunction detected! Notifying mission control.")
        if not Cloud_Seeding_Device_status:
            self.comms.send_status("[ALERT #02] Cloud Seeding Device malfunction detected! Notifying mission control.")
        if not Ionospheric_Particle_Collector_status:
            self.comms.send_status("[ALERT #03] Ionospheric_Particle_Collector malfunction detected! Notifying mission control.")

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




# Example usage (add this to your Spacecraft class):
# self.anomaly_detection = AnomalyDetectionSubsystem(self.comms_subsystem, self.power_subsystem)
# self.anomaly_detection.check_sensors(sensor1_ok, sensor2_ok) wawa
# self.anomaly_detection.handle_eclipse(is_sunlight_phase, is_charging)