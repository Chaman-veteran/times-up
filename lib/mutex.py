"""
    mutex.py
    Module implementing naive, non-atomic mutex.
"""

class Mutex:
    def __init__(self, value = 1):
        self.value = value
    
    def take(self):
        while self.value == 0:
            pass
        self.value -= 1
    
    def put(self, value = 1):
        self.value += value
    
    def get_value(self):
        return self.value
