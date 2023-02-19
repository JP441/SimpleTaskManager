import tkinter as tk
import customtkinter as ctk
import MainMenuFrame
class Main_Window:
    def __init__(self):
        self.main_window = ctk.CTk()
        self.main_window.geometry("700x550")
        self.main_window.resizable(height=False, width=False)
        self.main_window.title('Simple Task Manager')
        
        #Frames
        self.mmf = MainMenuFrame.Main_Menu_Frame(self.main_window)

        #Adding frames to window
        self.mmf.pack(side='top', pady=150, fill='x')




        self.main_window.mainloop()
    
STM = Main_Window()