import math
class payload:
    def __init__(self, name, mass, volume):
        self.name = name
        self.mass = mass
        self.volume = volume

    def __str__(self):
        return f"Payload(name={self.name}, mass={self.mass}, volume={self.volume})"