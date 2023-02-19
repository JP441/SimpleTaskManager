import tkinter as tk
import customtkinter as ctk
class Main_Menu_Frame(ctk.CTkFrame):
    def __init__(self, master_window):
        super().__init__(master_window)

        #PhotoImage

        task_image = tk.PhotoImage(file="C:\\Users\\jerma\\OneDrive\\Documents\\GitHub\\SimpleTaskManager\\core\\Images\\task.png")
        weather_image = tk.PhotoImage(file="C:\\Users\\jerma\\OneDrive\\Documents\\GitHub\\SimpleTaskManager\\core\\Images\\weather.png")
        birthday_image = tk.PhotoImage(file="C:\\Users\\jerma\\OneDrive\\Documents\\GitHub\\SimpleTaskManager\\core\\Images\\birthday.png") 
        
        #Buttons 
        self.task_manager_btn = ctk.CTkButton(master=self, width=200, height=200, font=('Arial Black', -18), text='Task Manager', compound='bottom', image=task_image)
        self.weather_btn = ctk.CTkButton(master=self, width=200, height=200, font=('Arial Black', -18), text='Weather', compound='bottom', image=weather_image)
        self.birthday_btn = ctk.CTkButton(master=self, width=200, height=200, font=('Arial Black', -18), text='Birthday Tracker', compound='bottom', image=birthday_image)

        #Adding widgets to frames
        self.task_manager_btn.grid(row=0, column=0, padx=17)
        self.weather_btn.grid(row=0, column=1, padx=17)
        self.birthday_btn.grid(row=0, column=2, padx=17)
        

