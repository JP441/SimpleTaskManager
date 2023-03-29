import tkinter as tk
import tkinter.ttk as ttk
import customtkinter as ctk
from datetime import datetime
from SettingsWindow import Settings_window
from itertools import count

class Task_Tree:
    def __init__(self, master):
        self.newid = count()
        self.tree = ttk.Treeview(master, columns=('due_date', 'tag'))
        #column 1 (Task)
        self.tree.column('#0', anchor='center')
        self.tree.heading('#0', text='Task')
        #column 2 (Task)
        self.tree.column('due_date', anchor='center')
        self.tree.heading('due_date', text='Due Date')
        #column 3 (Task)
        self.tree.column('tag', anchor='center')
        self.tree.heading('tag', text='Tag')
        #tree colours
        self.tree.tag_configure('red', background='red', foreground='white')
        self.tree.tag_configure('yellow', background=Settings_window.medium_bg_colour, foreground=Settings_window.medium_fg_colour)
        self.tree.tag_configure('green', background='green', foreground='white')
        #scroll
        self.scroll = ctk.CTkScrollbar(master, command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scroll.set)
        #combobox
        self.sort_combo = ctk.CTkComboBox(master, values=('Due First', 'Due Last', 'By Tag (Asc)', 'By Tag (Desc)'), command=self.sort_by)
        self.sort_combo.set('Sort By: ')

        #geometry 
        self.tree.grid(row=1,column=0)
        self.scroll.grid(row=1, column=1, sticky='ns')
        self.sort_combo.grid(row=0, column=0, sticky='e')

        #bindings
        # self.sort_combo.bind('<<ComboboxSelected>>', self.sort_by)

    def set_tree_medium_colour(self, bg_colour, fg_colour):
        self.tree.tag_configure('yellow', background=bg_colour, foreground=fg_colour)

    def insert_into_tree(self, items):
        """function compares todays date with each tasks date. If todays date and the due date are equal then the task will be marked with a red tag,
        this will also be the case if todays date is greater than the tasks due date. If the tasks are not marked red then some more checks are peformed
        for task tag allocation.
        """
        today = datetime.now().date()
        yellow_days = Settings_window.yellow_days
        green_days = Settings_window.green_days
        for t in items:
            task_date = datetime.strptime(t['due_date'], '%d/%m/%y').date()
            delta = task_date - today
            if today >= task_date:
                self.tree.insert(parent='', index='end', iid=next(self.newid), text=t['task'], values=(t['due_date'], t['tag']), tags='red')
            elif delta.days <= yellow_days:
                self.tree.insert(parent='', index='end', iid=next(self.newid), text=t['task'], values=(t['due_date'], t['tag']), tags='yellow')  
            elif delta.days <= green_days:
                self.tree.insert(parent='', index='end', iid=next(self.newid), text=t['task'], values=(t['due_date'], t['tag']), tags='green')    
            else:
                self.tree.insert(parent='', index='end', iid=next(self.newid), text=t['task'], values=(t['due_date'], t['tag']))
    
    def remove_task(self, event):
        selected = self.tree.selection()
        for task in selected:
            self.tree.delete(task)

    def remove_all(self):
        selected = self.tree.get_children()
        for task in selected:
            self.tree.delete(task)

    def store_tree(self):
        """
        Gets all the children from the TreeView and creates a list of dictionaries with them. Each dictionary contains one task.
        The list is returned for future manipulation 
        """
        task_list = []
        selected = self.tree.get_children()
        for t in selected:
            task_list.append({
                'task':self.tree.item(t)['text'], 
                'due_date':self.tree.item(t)['values'][0], 
                'tag':self.tree.item(t)['values'][1]
                })
        return task_list

    def refresh_tree(self):
        tree_data = self.store_tree()
        self.remove_all()
        self.insert_into_tree(tree_data)


    def sort_by(self, event):
        sort_by = self.sort_combo.get()
        task_list = self.store_tree()
        self.remove_all()
        if sort_by == 'Due First':
            task_list.sort(key=lambda x: datetime.strptime(x['due_date'], '%d/%m/%y'))
        elif sort_by == 'Due Last':
            task_list.sort(key=lambda x: datetime.strptime(x['due_date'], '%d/%m/%y'), reverse=True)
        elif sort_by == 'By Tag (Asc)':
            task_list.sort(key=lambda x: x['tag'].lower())
        elif sort_by == 'By Tag (Desc)':
            task_list.sort(key=lambda x: x['tag'].lower(), reverse=True)
        self.insert_into_tree(task_list)
