import tkinter
import tkinter.ttk
from customtkinter import CTk, CTkFrame, CTkLabel, CTkButton, CTkEntry, CTkInputDialog 
from WarningMessage import Warning_Message
from csv import DictReader, DictWriter
from tkcalendar import DateEntry
from TaskTree import Task_Tree
from SettingsWindow import Settings_window


class Simple_Task_Manager:
    def __init__(self):
        #Lists
        self.tasks = []
        
        #window
        self.window = CTk()
        self.window.title('Simple Task Manager')
        self.window.resizable(height=False, width=False)
        self.centre_window()

        #TopLevel 
        self.settings = None

        #Frames
        self.north_frame = CTkFrame(master=self.window)
        self.south_frame = CTkFrame(master=self.window)

        #Widgets
        self.north_tree = Task_Tree(self.north_frame)
    
        #labels
        self.task_label = CTkLabel(text="Task:", master=self.south_frame)
        self.due_date_label = CTkLabel(text="Due Date:", master=self.south_frame)
        self.tag_label = CTkLabel(self.south_frame, text='Tag:')

        #Buttons
        self.create_task_btn = CTkButton(text="Create Task", master=self.south_frame)
        self.remove_task_btn = CTkButton(self.south_frame, text='Remove Task')
        self.settings_btn = CTkButton(self.south_frame, text='Settings')
        self.search_btn = CTkButton(self.south_frame, text="Search Tag")
        self.show_all_btn = CTkButton(self.south_frame, text="Show All Tasks")
        self.help_btn = CTkButton(self.south_frame, text="Help")
        #entrys
        self.task_ent = CTkEntry(width=250, master=self.south_frame)
        self.tag_ent = CTkEntry(width=250, master=self.south_frame)
        self.calendar = DateEntry(self.south_frame, date_pattern='dd/mm/yy', showweeknumbers=False)

        #Adding frames to window
        self.north_frame.pack()
        self.south_frame.pack(anchor='center', fill='y', pady=10)

        #Adding widgets to frames
        self.task_label.grid(row=0, column=0, pady=3,)
        self.task_ent.grid(row=0, column=1, pady=5)
        self.tag_label.grid(row=1, column=0)
        self.tag_ent.grid(row=1, column=1)
        self.due_date_label.grid(row=2, column=0, pady=3)
        self.calendar.grid(row=2, column=1, pady=3)
        self.create_task_btn.grid(row=3, column=0, padx=40, pady=5)
        self.remove_task_btn.grid(row=3, column=1, padx=40, pady=5)
        self.settings_btn.grid(row=3, column=2, padx=40, pady=5)
        self.search_btn.grid(row=4, column=0, padx=40, pady=5)
        self.show_all_btn.grid(row=4, column=1, padx=40, pady=5)
        self.help_btn.grid(row=4, column=2, padx=40, pady=5)

        #Bindings
        #Button Bindings
        self.create_task_btn.bind('<Button-1>', self.create_task)
        self.remove_task_btn.bind('<Button-1>', self.north_tree.remove_task)
        self.settings_btn.bind('<Button-1>', self.settings_open)
        self.search_btn.bind('<Button-1>', self.search)
        self.show_all_btn.bind('<Button-1>', self.show_all)
        #keyboard Bindings
        self.window.bind('<Delete>', self.north_tree.remove_task)
        self.task_ent.bind('<Return>', self.create_task)
        self.tag_ent.bind('<Return>', self.create_task)
        #Window Protocols
        self.window.after_idle(self.get_data)
        self.window.protocol("WM_DELETE_WINDOW", self.write_data)

        self.window.mainloop()

    #Functions
    def centre_window(self):
        app_width = 700
        app_height = 550
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        xcoords = int((screen_width - app_width) / 2)
        ycoords = int((screen_height - app_height) / 2)       
        self.window.geometry(f"{app_width}x{app_height}+{xcoords}+{ycoords}") 

    def get_task(self):
        return self.task_ent.get()

    def get_date(self):
        date = self.calendar.get_date()
        date = date.strftime('%d/%m/%y')
        return date

    def get_tag(self):
        return self.tag_ent.get()

    def create_task(self, event):
        task = self.get_task().strip()
        if task:
            date = self.get_date()
            tag = self.get_tag().strip()
            temp_dict = [{'task':task, 'due_date':date, 'tag':tag}]
            self.north_tree.insert_into_tree(temp_dict)
            self.north_tree.sort_by() 
            self.task_ent.delete(0, 'end') 
            self.tag_ent.delete(0, 'end')
        else:
            rootx = self.window.winfo_rootx() + 200
            rooty = self.window.winfo_rooty()
            wm = Warning_Message(self.window, rootx, rooty,'No Task Inputted', 'You cannot leave the task field blank')
            wm.grab_set()

    def settings_open(self, event):
        global settings
        if not Settings_window.is_displayed:
            settings = Settings_window(self.window, self.window.winfo_rootx(), self.window.winfo_rooty())
            settings.save_btn.bind('<Button-1>' , self.refresh)
            # settings.grab_set()
  
    #Reading And Writing Data
    def write_data(self):
        if not self.tasks:
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
        else:
            with open('tree_data.csv', 'w', newline='') as file:
                fieldnames = ['task', 'due_date', 'tag']
                dict_writer = DictWriter(file, fieldnames=fieldnames)
                dict_writer.writeheader()
                for t in self.tasks:
                    dict_writer.writerow({
                    'task':t['task'], 
                    'due_date':t['due_date'],
                    'tag':t['tag']
                    }) 
        self.window.destroy()
            
    def get_data(self):
        try:
            with open('settings_save.csv', 'r', newline='') as file:
                reader = DictReader(file)
                for setting in reader:
                    Settings_window.red_days = int(setting['red_days'])
                    Settings_window.yellow_days = int(setting['yellow_days'])
                    Settings_window.green_days = int(setting['green_days'])
                    Settings_window.high_bg_colour = setting['high_bg_colour']
                    Settings_window.high_fg_colour = setting['high_fg_colour']
                    Settings_window.medium_bg_colour = setting['medium_bg_colour']
                    Settings_window.medium_fg_colour = setting['medium_fg_colour']
                    Settings_window.low_bg_colour = setting['low_bg_colour']
                    Settings_window.low_fg_colour = setting['low_fg_colour'].strip()
                self.setTreeColours()
        except FileNotFoundError:
            pass

        try:
            with open('tree_data.csv', 'r', newline='') as file:
                dict_reader = DictReader(file)
                self.north_tree.insert_into_tree(dict_reader)
        except FileNotFoundError:
            pass

    def refresh(self, event):
        settings.save()
        self.setTreeColours()
        self.north_tree.refresh_tree()

    def setTreeColours(self):
        self.north_tree.set_tree_high_colour(Settings_window.high_bg_colour, Settings_window.high_fg_colour)
        self.north_tree.set_tree_medium_colour(Settings_window.medium_bg_colour, Settings_window.medium_fg_colour)
        self.north_tree.set_tree_low_colour(Settings_window.low_bg_colour, Settings_window.low_fg_colour)
    
    """This function disables the search button, remove button and create task button. It also removes their commands. Window key commands are also disabled"""
    def disable_buttons(self):
        self.search_btn.configure(state="disabled")
        self.search_btn.unbind("<Button-1>", None)        
        self.remove_task_btn.configure(state="disabled")
        self.remove_task_btn.unbind("<Button-1>", None)
        self.task_ent.delete(0, 'end')
        self.tag_ent.delete(0, 'end')
        self.task_ent.configure(state="disabled")
        self.tag_ent.configure(state="disabled")
        self.window.unbind('<Delete>', None)
        self.create_task_btn.configure(state="disabled")
        self.create_task_btn.unbind("<Button-1>", None)

    """This does the opposite of disable buttons, it reinstates the removed commands also"""
    def enable_buttons(self):
        self.create_task_btn.configure(state="normal")
        self.create_task_btn.bind('<Button-1>', self.create_task)
        self.search_btn.configure(state="normal")
        self.search_btn.bind('<Button-1>', self.search)
        self.remove_task_btn.configure(state="normal")
        self.remove_task_btn.bind('<Button-1>', self.north_tree.remove_task)
        self.task_ent.configure(state="normal")
        self.tag_ent.configure(state="normal")
        self.window.bind('<Delete>', self.north_tree.remove_task)

    def search(self, event):
        matched_tasks = []
        search_dialog = CTkInputDialog(text="Please enter a tag you would like to search for?", title="Tag Search") 
        search_dialog.geometry(f'320x220+{self.window.winfo_rootx()}+{self.window.winfo_rooty()}')
        inputted_data = search_dialog.get_input()
        if inputted_data != None:
            tree_tasks = self.north_tree.tree.get_children()
            if tree_tasks:
                for t in tree_tasks:
                    self.tasks.append({
                        'task':self.north_tree.tree.item(t)['text'], 
                        'due_date':self.north_tree.tree.item(t)['values'][0], 
                        'tag':self.north_tree.tree.item(t)['values'][1]
                        })
                for t in tree_tasks:
                    if inputted_data.lower().strip() == self.north_tree.tree.item(t)['values'][1].lower().strip():
                        matched_tasks.append({
                        'task':self.north_tree.tree.item(t)['text'], 
                        'due_date':self.north_tree.tree.item(t)['values'][0], 
                        'tag':self.north_tree.tree.item(t)['values'][1]
                        })
                self.north_tree.remove_all()
                self.north_tree.insert_into_tree(matched_tasks)
                self.disable_buttons()

    def show_all(self, event):
        if self.tasks:
            self.north_tree.remove_all()
            self.north_tree.insert_into_tree(self.tasks)
            self.enable_buttons()
            self.tasks.clear()
        




    

if __name__ == '__main__':
    test = Simple_Task_Manager()
        
    


