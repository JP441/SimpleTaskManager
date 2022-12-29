import tkinter as tk
import tkinter.ttk as ttk
from tkinter.messagebox import showerror 
import itertools
from csv import DictReader, DictWriter
from tkcalendar import DateEntry
from datetime import datetime
from SettingsWindow import Settings_window

newid = itertools.count()

#functions
def create_task(*args):
    task = task_ent.get()
    if task:
        date = calendar.get_date()
        date = date.strftime('%d/%m/%y')
        tag = tag_ent.get()
        temp_dict = [{'task':task, 'due_date':date, 'tag':tag}]
        insert_into_tree(temp_dict)
        task_ent.delete(0, 'end') 
        tag_ent.delete(0, 'end')
    else:
        showerror(title='No Task', message='You cannot leave the task field blank')
        print('You must not leave task field blank')

def remove_task(*args):
    selected = tree.selection()
    for task in selected:
        tree.delete(task)

def remove_all():
    selected = tree.get_children()
    for task in selected:
        tree.delete(task)


def settings_open():
    if Settings_window.is_open == False:
        global settings
        settings = Settings_window(window, window.winfo_rootx(), window.winfo_rooty())
        settings.save_btn.bind('<Button-1>' , refresh_tree)


#Reading and writing data
def write_data():
    selected = tree.get_children()
    with open('tree_data.csv', 'w', newline='') as file:
        fieldnames = ['task', 'due_date', 'tag']
        dict_writer = DictWriter(file, fieldnames=fieldnames)
        dict_writer.writeheader()
        for t in selected:
            dict_writer.writerow({
            'task':tree.item(t)['text'], 
            'due_date':tree.item(t)['values'][0],
            'tag':tree.item(t)['values'][1]
            })
    window.destroy()
        
def get_data():
    try:
        with open('tree_data.csv', 'r', newline='') as file:
            dict_reader = DictReader(file)
            insert_into_tree(dict_reader)
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

    refresh_tree()

def insert_into_tree(items):
    today = datetime.now().date()
    yellow_days = Settings_window.yellow_days
    green_days = Settings_window.green_days
    for t in items:
        task_date = datetime.strptime(t['due_date'], '%d/%m/%y').date()
        delta = task_date - today
        if today >= task_date:
            tree.insert(parent='', index='end', iid=next(newid), text=t['task'], values=(t['due_date'], t['tag']), tags='red')
        elif delta.days <= yellow_days:
            tree.insert(parent='', index='end', iid=next(newid), text=t['task'], values=(t['due_date'], t['tag']), tags='yellow')  
        elif delta.days <= green_days:
            tree.insert(parent='', index='end', iid=next(newid), text=t['task'], values=(t['due_date'], t['tag']), tags='green')    
        else:
            tree.insert(parent='', index='end', iid=next(newid), text=t['task'], values=(t['due_date'], t['tag']))

    

def sort_by_date(event):
    sort_by = sort_combo.get()
    task_list = store_tree()
    remove_all()
    if sort_by == 'Due First':
        task_list.sort(key=lambda x: datetime.strptime(x['due_date'], '%d/%m/%y'))
    elif sort_by == 'Due Last':
        task_list.sort(key=lambda x: datetime.strptime(x['due_date'], '%d/%m/%y'), reverse=True)
    elif sort_by == 'By Tag (Asc)':
        task_list.sort(key=lambda x: x['tag'].lower())
    elif sort_by == 'By Tag (Desc)':
        task_list.sort(key=lambda x: x['tag'].lower(), reverse=True)
    insert_into_tree(task_list)

def store_tree():
    task_list = []
    selected = tree.get_children()
    for t in selected:
        task_list.append({
            'task':tree.item(t)['text'], 
            'due_date':tree.item(t)['values'][0], 
            'tag':tree.item(t)['values'][1]
            })
    return task_list

def refresh_tree(*args):
    try:
        settings.save()
    except NameError:
        pass
    tree_data = store_tree()
    remove_all()
    insert_into_tree(tree_data)

def get_task(self):
    return task_ent.get()

    


#window
window = tk.Tk()
window.resizable(height=False, width=False)
window.geometry("700x550")

#Image
settings_img = tk.PhotoImage(file = r"C:\Users\jerma\OneDrive\Documents\GitHub\SimpleTaskManager\core\Images\settings_cog.png")
settings_img_resized = settings_img.subsample(3,3)

#Toplevel



#Frames
north_frame = tk.Frame(master=window)
south_frame = tk.Frame(master=window)

#Widgets
#combobox
sort_combo = ttk.Combobox(north_frame, values=('Due First', 'Due Last', 'By Tag (Asc)', 'By Tag (Desc)'))
sort_combo.set('Sort By: ')

#Tree and Scrollbar
tree = ttk.Treeview(master=north_frame, columns=( 'due_date', 'tag'))
scroll = ttk.Scrollbar(north_frame, orient='vertical', command=tree.yview)
tree.configure(yscrollcommand=scroll.set)
#scroll config
#column 1 (Task)
tree.column('#0', anchor='center')
tree.heading('#0', text='Task')
#column 2 (Task)
tree.column('due_date', anchor='center')
tree.heading('due_date', text='Due Date')
#column 3 (Task)
tree.column('tag', anchor='center')
tree.heading('tag', text='Tag')

#tree colours
tree.tag_configure('red', background='red', foreground='white')
tree.tag_configure('yellow', background='yellow')
tree.tag_configure('green', background='green', foreground='white')

#labels
task_label = tk.Label(text="Task:", master=south_frame)
due_date_label = tk.Label(text="Due Date:", master=south_frame)
tag_label = tk.Label(south_frame, text='Tag:')

#Buttons
create_task_btn = tk.Button(text="Create Task", master=south_frame, command=create_task)
remove_task_btn = tk.Button(south_frame, text='Remove Task', command=remove_task)
settings_btn = tk.Button(south_frame, image=settings_img_resized, command=settings_open)
#entrys
task_ent = tk.Entry(width=50, master=south_frame)
calendar = DateEntry(south_frame, date_pattern='dd/mm/yy')
tag_ent = tk.Entry(south_frame)

#Adding frames to window
north_frame.pack()
south_frame.pack()

#Adding widgets to frames
sort_combo.grid(row=0, column=0, sticky='e')
tree.grid(row=1,column=0)
scroll.grid(row=1, column=1, sticky='ns')
task_label.grid(row=0, column=0, pady=3,)
due_date_label.grid(row=1, column=0, pady=3)
task_ent.grid(row=0, column=1, pady=5)
tag_label.grid(row=2, column=0)
tag_ent.grid(row=2, column=1)
create_task_btn.grid(row=3, column=0, padx=5, pady=5)
remove_task_btn.grid(row=3, column=1, padx=5, pady=5)
settings_btn.grid(row=3, column=2, padx=5, pady=5)
calendar.grid(row=1, column=1)


#bindings
sort_combo.bind('<<ComboboxSelected>>', sort_by_date)
window.bind('<Delete>', remove_task)
task_ent.bind('<Return>', create_task)
tag_ent.bind('<Return>', create_task)
window.after_idle(get_data)
window.protocol("WM_DELETE_WINDOW", write_data)

window.mainloop()



