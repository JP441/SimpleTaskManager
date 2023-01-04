import tkinter as tk
import tkinter.ttk as ttk
from tkinter.messagebox import showerror 
from csv import DictReader, DictWriter
from tkcalendar import DateEntry
from datetime import datetime
from TaskTree import Task_Tree
from SettingsWindow import Settings_window


class Simple_Task_Manager:
    def __init__(self):
        #window
        self.window = tk.Tk()
        self.window.resizable(height=False, width=False)
        self.window.geometry("700x550")

        #Image
        self.settings_img = tk.PhotoImage(file = r"C:\Users\jerma\OneDrive\Documents\GitHub\SimpleTaskManager\core\Images\settings_cog.png")
        self.settings_img_resized = self.settings_img.subsample(3,3)

        #Frames
        self.north_frame = tk.Frame(master=self.window)
        self.south_frame = tk.Frame(master=self.window)

        #Widgets
        self.north_tree = Task_Tree(self.north_frame)
    
        #labels
        self.task_label = tk.Label(text="Task:", master=self.south_frame)
        self.due_date_label = tk.Label(text="Due Date:", master=self.south_frame)
        self.tag_label = tk.Label(self.south_frame, text='Tag:')

        #Buttons
        self.create_task_btn = tk.Button(text="Create Task", master=self.south_frame)
        self.remove_task_btn = tk.Button(self.south_frame, text='Remove Task')
        self.settings_btn = tk.Button(self.south_frame, image=self.settings_img_resized)
        #entrys
        self.task_ent = tk.Entry(width=50, master=self.south_frame)
        self.calendar = DateEntry(self.south_frame, date_pattern='dd/mm/yy')
        self.tag_ent = tk.Entry(self.south_frame)

        #Adding frames to window
        self.north_frame.pack()
        self.south_frame.pack()

        #Adding widgets to frames
        self.task_label.grid(row=0, column=0, pady=3,)
        self.due_date_label.grid(row=1, column=0, pady=3)
        self.task_ent.grid(row=0, column=1, pady=5)
        self.tag_label.grid(row=2, column=0)
        self.tag_ent.grid(row=2, column=1)
        self.create_task_btn.grid(row=3, column=0, padx=5, pady=5)
        self.remove_task_btn.grid(row=3, column=1, padx=5, pady=5)
        self.settings_btn.grid(row=3, column=2, padx=5, pady=5)
        self.calendar.grid(row=1, column=1)


        #Bindings
        #Button Bindings
        self.create_task_btn.bind('<Button-1>', self.create_task)
        self.remove_task_btn.bind('<Button-1>', self.north_tree.remove_task)
        self.settings_btn.bind('<Button-1>', self.settings_open)
        #keyboard Bindings
        self.window.bind('<Delete>', self.north_tree.remove_task)
        self.task_ent.bind('<Return>', self.create_task)
        self.tag_ent.bind('<Return>', self.create_task)
        #Window Protocols
        self.window.after_idle(self.get_data)
        self.window.protocol("WM_DELETE_WINDOW", self.write_data)

        self.window.mainloop()


    #Functions

    def get_task(self):
        return self.task_ent.get()

    def get_date(self):
        date = self.calendar.get_date()
        date = date.strftime('%d/%m/%y')
        return date

    def get_tag(self):
        return self.tag_ent.get()

    def create_task(self, event):
        task = self.get_task()
        if task:
            date = self.get_date()
            tag = self.get_tag()
            temp_dict = [{'task':task, 'due_date':date, 'tag':tag}]
            self.north_tree.insert_into_tree(temp_dict)
            self.task_ent.delete(0, 'end') 
            self.tag_ent.delete(0, 'end')
        else:
            showerror(title='No Task', message='You cannot leave the task field blank')


    def settings_open(self, event):
        if Settings_window.is_open == False:
            global settings
            settings = Settings_window(self.window, self.window.winfo_rootx(), self.window.winfo_rooty())
            settings.save_btn.bind('<Button-1>' , self.refresh)


    #Reading And Writing Data
    def write_data(self):
        selected = self.north_tree.tree.get_children()
        with open('tree_data.csv', 'w', newline='') as file:
            fieldnames = ['task', 'due_date', 'tag']
            dict_writer = DictWriter(file, fieldnames=fieldnames)
            dict_writer.writeheader()
            for t in selected:
                dict_writer.writerow({
                'task':self.north_tree.tree.item(t)['text'], 
                'due_date':self.north_tree.tree.item(t)['values'][0],
                'tag':self.north_tree.tree.item(t)['values'][1]
                })
        self.window.destroy()
            
    def get_data(self):
        try:
            with open('tree_data.csv', 'r', newline='') as file:
                dict_reader = DictReader(file)
                self.north_tree.insert_into_tree(dict_reader)
        except FileNotFoundError:
            pass

        try:
            with open('settings_save.csv', 'r', newline='') as file:
                reader = DictReader(file)
                for setting in reader:
                    Settings_window.yellow_days = int(setting['yellow_days'])
                    Settings_window.green_days = int(setting['green_days'])
        except FileNotFoundError:
            pass

    def refresh(self, event):
        settings.save()
        self.north_tree.refresh_tree()

if __name__ == '__main__':
    test = Simple_Task_Manager()
        
    


