from datetime import datetime, timedelta
import tkinter as tk

class Timer:
    def __init_gui__(self, window):
        self.window = window
        label = tk.Label(window,
                       font=('calibri', 40, 'bold'),
                       background='purple',
                       foreground='white')
        self.label = label

    def __init__(self, window):
        self.start_time : datetime = None
        self.end_time : datetime = None
        self.__init_gui__(window)
    
    def draw(self):
        self.label.pack()
    
    def update(self):
        self.label.config(text=f'{self.get_remaining_time():.2f}s')
    
    def clear(self):
        self.label.pack_forget()

    def start(self, duration : int = 30):
        self.start_time = datetime.now()
        self.end_time = self.start_time + timedelta(seconds=duration)
    
    def get_remaining_time(self) -> int:
        remaining_time : timedelta = self.end_time - datetime.now() if self.end_time != None \
                                    else timedelta(0)
        return max(0, remaining_time.total_seconds())
    
    def reset(self, duration : int = 30):
        self.start_time=datetime.now()
        self.end_time = self.start_time + timedelta(seconds=duration)
