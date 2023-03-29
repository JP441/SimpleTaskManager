import tkinter
from customtkinter import CTkToplevel, CTkFrame, CTkImage, CTkButton, CTkLabel
from winsound import MessageBeep
from PIL import Image
class Warning_Message(CTkToplevel):
    is_displayed = False
    def __init__(self, master, window_x, window_y, mTitle, mText, mButtonText='Ok'):
        super().__init__(master)
        Warning_Message.is_displayed = True
        #Setting Up The Top Level
        self.resizable(False, False)
        self.geometry(f'340x160+{window_x}+{window_y}')
        self.title(mTitle)
        MessageBeep()
        self.after(100, self.focus)

        #Frame
        frame = CTkFrame(self, fg_color='transparent')

        #Image
        dark_icon_path = "C:\\Users\\jerma\OneDrive\\Documents\\GitHub\\SimpleTaskManager\\core\\Images\\warning_dark.png"
        light_icon_path = "C:\\Users\\jerma\OneDrive\\Documents\\GitHub\\SimpleTaskManager\\core\\Images\\warning_light.png"
        warning_icon = CTkImage(dark_image=Image.open(dark_icon_path),
                                light_image=Image.open(light_icon_path),
                                size=(80,80))
        icon = CTkButton(frame, image=warning_icon, hover=False, text="", fg_color="transparent", width=50)

        #Label
        message = CTkLabel(frame, text=mText)

        #button
        ok_btn = CTkButton(frame, text=mButtonText)

        #Geometry
        frame.pack(fill='both', pady=15)
        icon.grid(row=0, column=0, sticky="w")
        message.grid(row=0, column=1)
        ok_btn.grid(row=1, column=1, sticky='we')

        #binding
        ok_btn.bind("<Button-1>", command=self.close_window)
        self.protocol("WM_DELETE_WINDOW", self.close_window)
        
        #Method
    def close_window(self, *args):
        Warning_Message.is_displayed = False
        self.destroy()