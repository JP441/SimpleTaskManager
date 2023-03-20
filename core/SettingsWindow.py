import tkinter as tk
import customtkinter as ctk
from csv import DictWriter
from CTkColorPicker import AskColor
class Settings_window(ctk.CTkToplevel):
    yellow_days = 3
    green_days = 4
    medium_bg_colour = 'yellow'
    is_open = False
    def __init__(self, master, window_x, window_y):
        super().__init__(master)

        Settings_window.is_open = True
        self.yellow_ent_num = Settings_window.yellow_days
        self.green_ent_num = Settings_window.green_days
        
        #Widgets
        #Frames
        self.notice_frame = ctk.CTkFrame(self)
        self.colour_frame = ctk.CTkFrame(self)
        # self.green_frame = ctk.CTkFrame(self.new_window)
        
        #Yellow Day Counter
        self.yellow_lbl = ctk.CTkLabel(master=self.notice_frame, text='Medium Priority Notice (Days): ', padx=5)
        self.yellow_plus_btn = ctk.CTkButton(master=self.notice_frame, text='+', width=5)
        self.yellow_ent = ctk.CTkEntry(self.notice_frame, justify='center')
        self.yellow_minus_btn = ctk.CTkButton(master=self.notice_frame, text='-', width=5)
        #Green Day Counter
        self.green_lbl = ctk.CTkLabel(master=self.notice_frame, text='Low Priority Notice (Days): ', padx=5)
        self.green_plus_btn = ctk.CTkButton(master=self.notice_frame, text='+', width=5)
        self.green_ent = ctk.CTkEntry(self.notice_frame, justify='center')
        self.green_minus_btn = ctk.CTkButton(master=self.notice_frame, text='-', width=5)

        #Medium Priority Colour Picker
        self.medium_colour_lbl = ctk.CTkLabel(master=self.colour_frame, text='Medium Priority Background Colour: ')
        self.medium_colour_btn = ctk.CTkButton(master=self.colour_frame, text='Pick', width=5)
        self.medium_bg_colour_ent = ctk.CTkEntry(master=self.colour_frame, width=150)
        


        self.save_btn = ctk.CTkButton(master=self.colour_frame, text='Save And Exit')


        #Geometry
        #frames
        self.geometry(f'500x400+{window_x}+{window_y}')
        self.notice_frame.pack(pady=10)
        self.colour_frame.pack(pady=10)
        
        
        #Medium Priority Notice
        self.yellow_lbl.grid(row=0, column=0, pady=3)
        self.yellow_minus_btn.grid(row=0, column=1, padx=3)
        self.yellow_ent.grid(row=0, column=2)
        self.yellow_plus_btn.grid(row=0, column=3, padx=3)
        
        #Low Priority Notice
        self.green_lbl.grid(row=1, column=0, pady=3)
        self.green_minus_btn.grid(row=1, column=1, padx=3)
        self.green_ent.grid(row=1, column=2)
        self.green_plus_btn.grid(row=1, column=3, padx=3)

        #Medium Priority Color Selection
        self.medium_colour_lbl.grid(row=0, column=0, pady=3)
        self.medium_colour_btn.grid(row=0, column=1, pady=3, padx=3)
        self.medium_bg_colour_ent.grid(row=0, column=2, pady=3, padx=3)

        #Save Button
        self.save_btn.grid(row=1, column=2, pady=3)


        self.yellow_ent.insert(0, str(self.yellow_ent_num))
        self.green_ent.insert(0, str(self.green_ent_num))
        self.medium_bg_colour_ent.insert(0, self.medium_bg_colour)
        
        #Bindings
        self.yellow_plus_btn.bind('<Button-1>', self.increment_yellow)
        self.yellow_minus_btn.bind('<Button-1>', self.decrement_yellow)
        self.green_plus_btn.bind('<Button-1>', self.increment_green)
        self.green_minus_btn.bind('<Button-1>', self.decrement_green)
        self.medium_colour_btn.bind('<Button-1>', self.set_medium_bg_colour)
        self.protocol("WM_DELETE_WINDOW", self.close_window)
        self.after_idle(self.focus)
    
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
        self.destroy()
        Settings_window.is_open = False 

    def save(self):
        Settings_window.yellow_days = self.yellow_ent_num
        Settings_window.green_days = self.green_ent_num
        Settings_window.medium_bg_colour = self.medium_bg_colour_ent.get()
        self.write_settings()
        self.close_window()
    
    def write_settings(self):
        with open('settings_save.csv', 'w', newline='') as file:
            field_names = ['yellow_days', 'green_days', 'medium_bg_colour']
            writer = DictWriter(file, fieldnames=field_names)
            writer.writeheader()
            writer.writerow({'yellow_days':self.yellow_ent_num, 'green_days':self.green_ent_num, 'medium_bg_colour':self.medium_bg_colour})

    def colour_picker(self):
        pick_colour = AskColor()
        return pick_colour.get()

    def set_medium_bg_colour(self, event):
        colour = self.colour_picker()
        if colour:
            self.medium_bg_colour_ent.delete(0, 'end')
            self.medium_bg_colour_ent.insert(0, colour)

    def get_medium_bg_colour():
        return Settings_window.medium_bg_colour
    


    




    




