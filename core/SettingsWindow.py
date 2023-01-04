import tkinter as tk
from csv import DictReader, DictWriter
class Settings_window:
    yellow_days = 3
    green_days = 4
    is_open = False
    def __init__(self, master, window_x, window_y):
        Settings_window.is_open = True
        self.yellow_ent_num = Settings_window.yellow_days
        self.green_ent_num = Settings_window.green_days
        
        #Widgets
        self.new_window = tk.Toplevel(master)
        #Frames
        self.yellow_frame = tk.Frame(self.new_window)
        self.green_frame = tk.Frame(self.new_window)
        #Yellow Day Counter
        self.yellow_lbl = tk.Label(master=self.yellow_frame, text='Yellow Days: ', padx=5)
        self.yellow_plus_btn = tk.Button(master=self.yellow_frame, text='+')
        self.yellow_ent = tk.Entry(self.yellow_frame, justify='center')
        self.yellow_minus_btn = tk.Button(master=self.yellow_frame, text='-')
        #Green Day Counter
        self.green_lbl = tk.Label(master=self.green_frame, text='Green Days: ', padx=5)
        self.green_plus_btn = tk.Button(master=self.green_frame, text='+')
        self.green_ent = tk.Entry(self.green_frame, justify='center')
        self.green_minus_btn = tk.Button(master=self.green_frame, text='-')
        


        self.save_btn = tk.Button(master=self.green_frame, text='Save And Exit')


        #Geometry
        #frames
        self.new_window.geometry(f'500x400+{window_x}+{window_y}')
        self.yellow_frame.pack(pady=10)
        self.green_frame.pack(pady=10)
        
        self.save_btn.pack(side='bottom')
        
        #Yellow
        self.yellow_lbl.pack(side='left')
        self.yellow_minus_btn.pack(side='left')
        self.yellow_ent.pack(side='left')
        self.yellow_plus_btn.pack(side='left')
        
        #Green
        self.green_lbl.pack(side='left')
        self.green_minus_btn.pack(side='left')
        self.green_ent.pack(side='left')
        self.green_plus_btn.pack(side='left')


        self.yellow_ent.insert(0, str(self.yellow_ent_num))
        self.green_ent.insert(0, str(self.green_ent_num))
        
        #Bindings
        self.yellow_plus_btn.bind('<Button-1>', self.increment_yellow)
        self.yellow_minus_btn.bind('<Button-1>', self.decrement_yellow)
        self.green_plus_btn.bind('<Button-1>', self.increment_green)
        self.green_minus_btn.bind('<Button-1>', self.decrement_green)
        self.new_window.protocol("WM_DELETE_WINDOW", self.close_window)
        # self.new_window.after_idle(self.read_settings)
    
    #Methods


    def increment_yellow(self, event):
        if self.yellow_ent_num < self.green_ent_num - 1: 
            self.yellow_ent.delete(0, 'end')
            self.yellow_ent_num += 1
            result = str(self.yellow_ent_num)
            self.yellow_ent.insert(0, result)   

    def decrement_yellow(self, event):
        if self.yellow_ent_num > 1:
            self.yellow_ent.delete(0, 'end')
            self.yellow_ent_num -= 1
            result = str(self.yellow_ent_num)
            self.yellow_ent.insert(0, result)

    def increment_green(self, event): 
        self.green_ent.delete(0, 'end')
        self.green_ent_num += 1
        result = str(self.green_ent_num)
        self.green_ent.insert(0, result)

    def decrement_green(self, event):
        if self.green_ent_num > self.yellow_ent_num + 1:
            self.green_ent.delete(0, 'end')
            self.green_ent_num -= 1
            result = str(self.green_ent_num)
            self.green_ent.insert(0, result)  

    def close_window(self):
        self.new_window.destroy()
        Settings_window.is_open = False 

    def save(self):
        Settings_window.yellow_days = self.yellow_ent_num
        Settings_window.green_days = self.green_ent_num
        self.write_settings()
        self.close_window()
    
    def write_settings(self):
        with open('settings_save.csv', 'w', newline='') as file:
            field_names = ['yellow_days', 'green_days']
            writer = DictWriter(file, fieldnames=field_names)
            writer.writeheader()
            writer.writerow({'yellow_days':self.yellow_ent_num, 'green_days':self.green_ent_num})

    # def read_settings(self):
    #     try:
    #         with open('settings_save.csv', 'r', newline='') as file:
    #             reader = DictReader(file)
    #             for setting in reader:
    #                 Settings_window.yellow_days = setting['yellow_days']
    #                 Settings_window.green_days = setting['green_days']
    #     except FileNotFoundError:
    #         pass


    




    




