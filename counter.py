import time
from datetime import datetime, timedelta

class Timer:
    def __init__(self):
        self.start_time = None
        self.end_time = None

    def start(self, duration : int = 30):
        self.start_time = datetime.now()
        self.end_time = self.start_time + timedelta(seconds=duration)
    
    def get_remaining_time(self):
        remaining_time = self.end_time - datetime.now()
        return max(0, remaining_time.total_seconds())
    
    def reset(self, duration : int = 30):
        self.start_time=datetime.now()
        self.end_time = self.start_time + timedelta(seconds=duration)

# timer = Timer()
# timer.start(30)
# print(timer.get_remaining_time())
# time.sleep(3)
# print(timer.get_remaining_time())
# timer.reset()
# time.sleep(1)
# print(timer.get_remaining_time())