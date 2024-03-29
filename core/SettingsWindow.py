import tkinter as tk
import customtkinter as ctk
from csv import DictWriter
from ColourChanger import Colour_Changer
from WarningMessage import Warning_Message
class Settings_window(ctk.CTkToplevel):
    red_days = 0
    yellow_days = 3
    green_days = 4
    high_bg_colour = '#FF0000'
    high_fg_colour = '#ffffff'
    medium_bg_colour = '#FFFF00'
    medium_fg_colour = '#000000'
    low_bg_colour = '#00862B'
    low_fg_colour = '#ffffff'
    is_displayed = False

    def __init__(self, master, window_x, window_y):
        super().__init__(master)
        self.red_ent_num = Settings_window.red_days
        self.yellow_ent_num = Settings_window.yellow_days
        self.green_ent_num = Settings_window.green_days
        self.title("Settings")
        Settings_window.is_displayed = True
        
        #Widgets
        #Frames
        self.main_frame = ctk.CTkFrame(self)
        self.notice_frame = ctk.CTkFrame(self.main_frame)
        self.high_frame = Colour_Changer(self.main_frame)
        self.medium_frame = Colour_Changer(self.main_frame)
        self.low_fame = Colour_Changer(self.main_frame)
        self.south_button_frame = ctk.CTkFrame(self.main_frame)

        #labels
        self.notice_lbl = ctk.CTkLabel(self.main_frame, font=('Helvetica', 15), text='Task Notification Thresholds')
        self.high_lbl = ctk.CTkLabel(self.main_frame, font=('Open Sans', 15),text='High Priority Colour Settings')
        self.medium_lbl = ctk.CTkLabel(self.main_frame, font=('Open Sans', 15),text='Medium Priority Colour Settings')
        self.low_lbl = ctk.CTkLabel(self.main_frame, font=('Open Sans', 15), text='Low Priority Colour Settings')
  
        #Red Day Counter
        self.red_lbl = ctk.CTkLabel(master=self.notice_frame, text='High Priority Notice (Days): ', padx=5)
        self.red_plus_btn = ctk.CTkButton(master=self.notice_frame, text='+', width=5)
        self.red_ent = ctk.CTkEntry(self.notice_frame, justify='center')
        self.red_minus_btn = ctk.CTkButton(master=self.notice_frame, text='-', width=5)

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

        #Buttons
        self.save_btn = ctk.CTkButton(master=self.south_button_frame, text='Save And Exit')
        self.reset_btn = ctk.CTkButton(master=self.south_button_frame, text='Reset Settings')


        #Geometry
        #TopLevel
        self.geometry(f'500x800+{window_x}+{window_y}')
        
        #frames
        self.main_frame.pack(fill='both', expand=True)
        self.pack_propagate(False)
        self.notice_lbl.pack(side='top', fill='none', pady=10)
        self.notice_frame.pack(side='top', fill='none', pady=10)
        self.high_lbl.pack(side='top', fill='none', pady=10)
        self.high_frame.pack(side='top', fill='none', pady=10)
        self.medium_lbl.pack(side='top', fill='none', pady=10)
        self.medium_frame.pack(side='top', fill='none', pady=10)
        self.low_lbl.pack(side='top', fill='none', pady=10)
        self.low_fame.pack(side='top', fill='none', pady=10)
        self.south_button_frame.pack(side='top', fill='none', pady=10)
        
        #High Priority Notice
        self.red_lbl.grid(row=0, column=0, pady=3)
        self.red_minus_btn.grid(row=0, column=1, padx=3)
        self.red_ent.grid(row=0, column=2)
        self.red_plus_btn.grid(row=0, column=3, padx=3)

        #Medium Priority Notice
        self.yellow_lbl.grid(row=1, column=0, pady=3)
        self.yellow_minus_btn.grid(row=1, column=1, padx=3)
        self.yellow_ent.grid(row=1, column=2)
        self.yellow_plus_btn.grid(row=1, column=3, padx=3)
        
        #Low Priority Notice
        self.green_lbl.grid(row=2, column=0, pady=3)
        self.green_minus_btn.grid(row=2, column=1, padx=3)
        self.green_ent.grid(row=2, column=2)
        self.green_plus_btn.grid(row=2, column=3, padx=3)

        #Save And Reset Button
        self.save_btn.grid(row=1, column=2, pady=3, padx=3)
        self.reset_btn.grid(row=1, column=3, pady=3, padx=3)

        #Inserting saved data into entrys
        self.set_entrys()
        
        #Bindings
        self.red_plus_btn.bind('<Button-1>', self.increment_red)
        self.red_minus_btn.bind('<Button-1>', self.decrement_red)
        self.yellow_plus_btn.bind('<Button-1>', self.increment_yellow)
        self.yellow_minus_btn.bind('<Button-1>', self.decrement_yellow)
        self.green_plus_btn.bind('<Button-1>', self.increment_green)
        self.green_minus_btn.bind('<Button-1>', self.decrement_green)
        self.reset_btn.bind('<Button-1>', self.restore_defaults)
        self.protocol("WM_DELETE_WINDOW", self.close_window)
        self.after_idle(self.focus)
    
    #Methods
    def increment_red(self, event):
        if self.red_ent_num < self.yellow_ent_num - 1:
            self.red_ent.configure(state='normal')
            self.red_ent.delete(0, 'end')
            self.red_ent_num += 1
            result = str(self.red_ent_num)
            self.red_ent.insert(0, result)
            self.red_ent.configure(state='readonly')

    def decrement_red(self, event):
        if self.red_ent_num > 0:
            self.red_ent.configure(state='normal')
            self.red_ent.delete(0, 'end')
            self.red_ent_num -= 1
            result = str(self.red_ent_num)
            self.red_ent.insert(0, result)
            self.red_ent.configure(state='readonly')

    def increment_yellow(self, event):
        if self.yellow_ent_num < self.green_ent_num - 1: 
            self.yellow_ent.configure(state='normal')
            self.yellow_ent.delete(0, 'end')
            self.yellow_ent_num += 1
            result = str(self.yellow_ent_num)
            self.yellow_ent.insert(0, result)
            self.yellow_ent.configure(state='readonly')  

    def decrement_yellow(self, event):
        if self.yellow_ent_num > self.red_ent_num + 1:
            self.yellow_ent.configure(state='normal')
            self.yellow_ent.delete(0, 'end')
            self.yellow_ent_num -= 1
            result = str(self.yellow_ent_num)
            self.yellow_ent.insert(0, result)
            self.yellow_ent.configure(state='readonly')

    def increment_green(self, event):
        self.green_ent.configure(state='normal') 
        self.green_ent.delete(0, 'end')
        self.green_ent_num += 1
        result = str(self.green_ent_num)
        self.green_ent.insert(0, result)
        self.green_ent.configure(state='readonly') 

    def decrement_green(self, event):
        if self.green_ent_num > self.yellow_ent_num + 1:
            self.green_ent.configure(state='normal') 
            self.green_ent.delete(0, 'end')
            self.green_ent_num -= 1
            result = str(self.green_ent_num)
            self.green_ent.insert(0, result)
            self.green_ent.configure(state='readonly') 
    
    def set_entrys(self):
        self.red_ent.configure(state='normal')
        self.yellow_ent.configure(state='normal')
        self.green_ent.configure(state='normal')
        self.red_ent.delete(0, 'end')
        self.yellow_ent.delete(0, 'end')
        self.green_ent.delete(0, 'end')
        self.red_ent.insert(0, str(self.red_ent_num))
        self.red_ent.configure(state='readonly')
        self.yellow_ent.insert(0, str(self.yellow_ent_num))
        self.yellow_ent.configure(state='readonly')
        self.green_ent.insert(0, str(self.green_ent_num))
        self.green_ent.configure(state='readonly')
        self.high_frame.set_bg_ent(Settings_window.high_bg_colour)
        self.high_frame.set_fg_ent(Settings_window.high_fg_colour)
        self.medium_frame.set_bg_ent(Settings_window.medium_bg_colour)
        self.medium_frame.set_fg_ent(Settings_window.medium_fg_colour)
        self.low_fame.set_bg_ent(Settings_window.low_bg_colour)
        self.low_fame.set_fg_ent(Settings_window.low_fg_colour)

    def restore_defaults(self, event):
        self.red_ent.configure(state='normal')
        self.yellow_ent.configure(state='normal')
        self.green_ent.configure(state='normal')
        self.red_ent.delete(0, 'end')
        self.yellow_ent.delete(0, 'end')
        self.green_ent.delete(0, 'end')
        self.red_ent_num = 0
        self.red_ent.insert(0, str(self.red_ent_num))
        self.red_ent.configure(state='readonly')
        self.yellow_ent_num = 3
        self.yellow_ent.insert(0, self.yellow_ent_num)
        self.yellow_ent.configure(state='readonly')
        self.green_ent_num = 4
        self.green_ent.insert(0, self.green_ent_num)
        self.green_ent.configure(state='readonly')
        self.high_frame.set_bg_ent('#FF0000')
        self.high_frame.set_fg_ent('#ffffff')
        self.medium_frame.set_bg_ent('#FFFF00')
        self.medium_frame.set_fg_ent('#000000')
        self.low_fame.set_bg_ent('#00862B')
        self.low_fame.set_fg_ent('#ffffff')

    def close_window(self):
        Settings_window.is_displayed = False
        self.destroy() 
        print(Settings_window.red_days, Settings_window.yellow_days, Settings_window.green_days)

    """This function gets values from entrys for the amount of days notice each priority level gives and each priority
    level's bg and fg colours. This function will save these values to the class varibles and write them to file. 
    This function checks that the hex colours are valid before saving them. If even one is not valid then it will throw
    an error message"""
    def save(self):
        high_bg_colour = self.high_frame.get_hex_colour('background')
        high_fg_colour = self.high_frame.get_hex_colour('foreground')
        medium_bg_colour = self.medium_frame.get_hex_colour('background')
        medium_fg_colour = self.medium_frame.get_hex_colour('foreground')
        low_bg_colour = self.low_fame.get_hex_colour('background')
        low_fg_colour = self.low_fame.get_hex_colour('foreground')
        if all([high_bg_colour, high_fg_colour, medium_bg_colour, medium_fg_colour, low_bg_colour, low_fg_colour]):
            Settings_window.high_bg_colour = high_bg_colour
            Settings_window.high_fg_colour = high_fg_colour
            Settings_window.medium_bg_colour = medium_bg_colour
            Settings_window.medium_fg_colour = medium_fg_colour
            Settings_window.low_bg_colour = low_bg_colour
            Settings_window.low_fg_colour = low_fg_colour
            Settings_window.red_days = self.red_ent_num
            Settings_window.yellow_days = self.yellow_ent_num
            Settings_window.green_days = self.green_ent_num
            self.write_settings()
            self.close_window()
        else:
            if not Warning_Message.is_displayed:
                rootx = self.master.winfo_rootx()
                rooty = self.master.winfo_rooty()
                Warning_Message(self, rootx, rooty, mTitle="Invalid Hex", mText="A Valid Hex Number Must Be Used" )

    def write_settings(self):
        with open('settings_save.csv', 'w', newline='') as file:
            field_names = ['yellow_days', 'green_days', 'red_days',
                           'high_bg_colour', 'high_fg_colour',
                           'medium_bg_colour', 'medium_fg_colour', 
                           'low_bg_colour', 'low_fg_colour']
            writer = DictWriter(file, fieldnames=field_names)
            writer.writeheader()
            writer.writerow({'red_days':self.red_ent_num, 'yellow_days':self.yellow_ent_num, 
                             'green_days':self.green_ent_num,
                             'high_bg_colour':self.high_bg_colour, 'high_fg_colour':self.high_fg_colour,
                             'medium_bg_colour':self.medium_bg_colour, 'medium_fg_colour':self.medium_fg_colour,
                             'low_bg_colour':self.low_bg_colour, 'low_fg_colour':self.low_fg_colour})
            
    def get_medium_bg_colour():
        return Settings_window.medium_bg_colour
    
    
    

    

    




    




