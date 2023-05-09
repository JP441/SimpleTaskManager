import tkinter as tk
import customtkinter as ctk
from csv import DictWriter
from ColourChanger import Colour_Changer
from WarningMessage import Warning_Message
class Settings_window(ctk.CTkToplevel):
    yellow_days = 3
    green_days = 4
    medium_bg_colour = '#FFFF00'
    medium_fg_colour = '#000000'
    low_bg_colour = '#FFFF00'
    low_fg_colour = '#000000'

    def __init__(self, master, window_x, window_y):
        super().__init__(master)

        self.yellow_ent_num = Settings_window.yellow_days
        self.green_ent_num = Settings_window.green_days
        self.title("Settings")
        #Widgets
        #labels
        self.notice_lbl = ctk.CTkLabel(self, font=('Helvetica', 15), text='Task Notification Thresholds')
        self.medium_lbl = ctk.CTkLabel(self, text='Medium Priority Colour Settings')
        self.low_lbl = ctk.CTkLabel(self, text='Low Priority Colour Settings')
        #Frames

        self.notice_frame = ctk.CTkFrame(self, 5000)
        self.medium_frame = Colour_Changer(self)
        self.low_fame = Colour_Changer(self)
        self.save_frame = ctk.CTkFrame(self)
        
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

        self.save_btn = ctk.CTkButton(master=self.save_frame, text='Save And Exit')


        #Geometry
        #frames
        self.geometry(f'500x400+{window_x}+{window_y}')
        self.notice_lbl.grid(row=0, column=1)
        self.notice_frame.grid(row=1,column=1, pady=10)
        self.medium_lbl.grid(row=2, column=1)
        self.medium_frame.grid(row=3,column=1,pady=10, sticky='we')
        self.low_lbl.grid(row=4, column=1)
        self.low_fame.grid(row=5,column=1,pady=10, sticky='we')
        self.save_frame.grid(row=6,column=1,pady=10)
        
        
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

        #Save Button
        self.save_btn.grid(row=1, column=2, pady=3)

        #Inserting saved data into entrys
        self.yellow_ent.insert(0, str(self.yellow_ent_num))
        self.green_ent.insert(0, str(self.green_ent_num))
        self.medium_frame.set_bg_ent(Settings_window.medium_bg_colour)
        self.medium_frame.set_fg_ent(Settings_window.medium_fg_colour)
        self.low_fame.set_bg_ent(Settings_window.low_bg_colour)
        self.low_fame.set_fg_ent(Settings_window.low_fg_colour)
        #Bindings
        self.yellow_plus_btn.bind('<Button-1>', self.increment_yellow)
        self.yellow_minus_btn.bind('<Button-1>', self.decrement_yellow)
        self.green_plus_btn.bind('<Button-1>', self.increment_green)
        self.green_minus_btn.bind('<Button-1>', self.decrement_green)
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

    """This function gets values from entrys for the amount of days notice each priority level gives and each priority
    level's bg and fg colours. This function will save these values to the class varibles and write them to file. 
    This function checks that the hex colours are valid before saving them. If even one is not valid then it will throw
    an error message"""
    def save(self):
        medium_bg_colour = self.medium_frame.get_hex_colour('background')
        medium_fg_colour = self.medium_frame.get_hex_colour('foreground')
        low_bg_colour = self.low_fame.get_hex_colour('background')
        low_fg_colour = self.low_fame.get_hex_colour('foreground')
        if all([medium_bg_colour, medium_fg_colour, low_bg_colour, low_fg_colour]):
            Settings_window.medium_bg_colour = medium_bg_colour
            Settings_window.medium_fg_colour = medium_fg_colour
            Settings_window.low_bg_colour = low_bg_colour
            Settings_window.low_fg_colour = low_fg_colour
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
            field_names = ['yellow_days', 'green_days', 'medium_bg_colour', 'medium_fg_colour', 'low_bg_colour', 'low_fg_colour']
            writer = DictWriter(file, fieldnames=field_names)
            writer.writeheader()
            writer.writerow({'yellow_days':self.yellow_ent_num, 'green_days':self.green_ent_num, 
                             'medium_bg_colour':self.medium_bg_colour, 'medium_fg_colour':self.medium_fg_colour,
                             'low_bg_colour':self.low_bg_colour, 'low_fg_colour':self.low_fg_colour})
            

    def get_medium_bg_colour():
        return Settings_window.medium_bg_colour
    
    
    

    

    




    




