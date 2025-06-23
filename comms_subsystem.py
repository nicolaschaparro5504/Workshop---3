class Communication_Subsystem:
    def __init__(self):
        self.connected = True
        self.power_subsystem = None
        self.sent_chars = []  # Creates an empty list ready to save the total length
        self._messages_before_summary = 4
        self._in_summary = False

    def attach_power_system(self, power_subsystem):  # Attach to power subsystem to consume battery
        self.power_subsystem = power_subsystem

    def send_status(self, status, skip_summary=False):
        """Performs the action of sending a message, also replaces the function print"""
        if not self.connected:
            print("[Comms] Error: Connection lost")
            return

        if self.power_subsystem is None:
            print("[Comms] Power subsystem not found")
            return

        char_count = len(status) # Gets the quantity of elements in the list
        self.sent_chars.append(char_count)

        print(f"[Comms] Transmitting ({char_count} chars): {status}")

    # Consumes energy only if the message is not a summary
        if not skip_summary:
            estimated_consumption = 0.005 * char_count
            if self.power_subsystem.consume_energy(estimated_consumption, log=False):
                print(f"[Power] Message energy cost: -{estimated_consumption:.4f}%")
            else:
                print("[Power] Not enough battery to send this message.")

        if len(self.sent_chars) >= self._messages_before_summary and not skip_summary:
            self.summarize()

    def summarize(self):
        """Method that counts all the characters used in send_status, 
        and measures the battery that costs to send them"""
        self._in_summary = True

        total_chars = sum(self.sent_chars)
        estimated_consumption = 0.0005 * total_chars  # Consumption per character

        print(f"[Comms] Total characters: {total_chars}")

        if self.power_subsystem:
            if self.power_subsystem.consume_energy(estimated_consumption, log=False):
                self.send_status(
                    f"[Power] Action Consumption: -{estimated_consumption:.2f}%, Battery Level: {self.power_subsystem.get_battery_level():.2f}%",
                    skip_summary=True
                )
            else:
                print("[Power] There's not enough battery to send.\n")

        self.sent_chars.clear()  # Clears the log of characters summarized
        self._in_summary = False  # Gets out of the summarize method



