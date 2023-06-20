import tkinter
from customtkinter import CTkLabel, CTkFrame, CTkButton, CTkEntry
from CTkColorPicker import AskColor
from WarningMessage import Warning_Message
import re
class Colour_Changer(CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        #Widgets
        #Background
        self.bg_label = CTkLabel(self, text='Background Colour')
        self.bg_colour_btn = CTkButton(self, text='Pick', width=5)
        self.bg_colour_ent = CTkEntry(self, width=150)
        
        #Foreground
        self.fg_label = CTkLabel(self, text='Text Colour')
        self.fg_colour_btn = CTkButton(self, text='Pick', width=5)
        self.fg_colour_ent = CTkEntry(self, width=150)

        #Preview
        self.preview_label = CTkLabel(self, text="Preview: ")
        self.preview_button = CTkButton(self, text="Text Colour", hover=False)

        #Geometry
        #Background settings
        self.bg_label.grid(row=1, column=0, pady=3, sticky='w')
        self.bg_colour_btn.grid(row=1, column=1, pady=3, padx=3)
        self.bg_colour_ent.grid(row=1, column=2, pady=3, padx=3)
        
        #Foreground setting
        self.fg_label.grid(row=2, column=0, pady=3, sticky='w')
        self.fg_colour_btn.grid(row=2, column=1, pady=3)
        self.fg_colour_ent.grid(row=2, column=2, pady=3)

        #Preview
        self.preview_label.grid(row=3, column=0, pady=3, sticky='w')
        self.preview_button.grid(row=3, column=1, pady=3, sticky='we', columnspan=2)


        #Bindings
        self.bg_colour_btn.bind('<Button-1>', self.set_colour) 
        self.fg_colour_btn.bind('<Button-1>', self.set_colour)

    """This function creates an instance of AskColor (colour wheel) and once the user has
    selected their colour and pressed ok"""
    def colour_picker(self):
        pick_colour = AskColor()
        return pick_colour.get()
    
    """Basic function takes a string that is a colour and inserts it into the entry. Also changes
    the preview button as well to match"""
    def set_bg_ent(self, string):
        self.bg_colour_ent.delete(0, 'end')
        self.bg_colour_ent.insert(0, string)
        self.preview_button.configure(fg_color=string)

    def set_fg_ent(self, string):
        self.fg_colour_ent.delete(0, 'end')
        self.fg_colour_ent.insert(0, string)
        self.preview_button.configure(text_color=string)
   
    """This function checks that the colour that was inputted is a valid Hex colour code.
    If it is then the function will return the Hex colour code as a string. Else it will
    return None"""
    def get_hex_colour(self, colour_type):
        if colour_type == 'background':     
            hexcolour = self.bg_colour_ent.get()
            x = re.search("^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$", hexcolour)
        elif colour_type == 'foreground':
            hexcolour = self.fg_colour_ent.get()
            x = re.search("^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$", hexcolour)    
            #re.search returns None if there is no match 
        if x:
            return x.string
    
    """This calls the colour picker and then if a colour is chosen and depending what button was pressed, 
    it will then it will clear the matching entry and insert the Hex code of the selected colour to that entry"""
    def set_colour(self, event):
        colour = self.colour_picker()
        if colour and event.widget.master == self.bg_colour_btn:
            self.set_bg_ent(colour)
        elif colour and event.widget.master == self.fg_colour_btn:
            self.set_fg_ent(colour)


