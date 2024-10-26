"""
    counter.py
    Module to display and manage the time counter.
"""

from datetime import datetime, timedelta
import tkinter as tk

DEFAULT_DURATION = 45

class Timer:
    def __init_gui__(self, window):
        self.window = window
        label = tk.Label(window,
                         font=('calibri', 40, 'bold'),
                         background='purple',
                         foreground='white')
        self.label = label

    def __init__(self, window):
        self.start_time : datetime | None = None
        self.end_time : datetime | None = None
        self.__init_gui__(window)
        self.duration = DEFAULT_DURATION
    
    def draw(self):
        self.label.pack()
    
    def update(self):
        self.label.config(text=f'{self.get_remaining_time():.1f}s')
    
    def clear(self):
        self.label.pack_forget()

    def start(self):
        self.start_time = datetime.now()
        self.end_time = self.start_time + timedelta(seconds=self.duration)
    
    def get_remaining_time(self) -> int:
        """
            Gives the time left for the current counter in seconds.
        """
        remaining_time : timedelta = self.end_time - datetime.now() if self.end_time != None \
                                    else timedelta(0)
        return max(0, remaining_time.total_seconds())
    
    def reset(self, duration : int = DEFAULT_DURATION):
        self.duration = duration
