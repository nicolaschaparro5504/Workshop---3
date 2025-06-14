from abc import ABC, abstractmethod

class Subsystem(ABC):
    def __init__(self, name):
        self.name = name
        self.status = "OFFLINE"
        self.fault = False
    
    @abstractmethod
    def update(self, dt):
        pass
    
    @abstractmethod
    def handle_event(self, event):
        pass
    
    def get_status(self):
        return {
            "name": self.name,
            "status": self.status,
            "fault": self.fault
        }
    
    def reset(self):
        self.fault = False
        self.status = "STANDBY"