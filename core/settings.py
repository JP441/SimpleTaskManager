import tkinter as tk
class Settings_window:
    def __init__(self, master):
        self.colour_frame = tk.Frame(master)
        self.yellow_plus_btn = tk.Button(master=self.colour_frame, text='+')
        self.yellow_ent = tk.Entry(self.colour_frame, justify='center')
        self.yellow_minus_btn = tk.Button(master=self.colour_frame, text='-')

        self.colour_frame.pack(pady=10)
        self.yellow_minus_btn.pack(side='left')
        self.yellow_ent.pack(side='left')
        self.yellow_plus_btn.pack(side='left')


