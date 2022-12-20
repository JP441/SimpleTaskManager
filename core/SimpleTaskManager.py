import tkinter as tk
import tkinter.ttk as ttk
import itertools
import csv
from tkcalendar import DateEntry
from datetime import datetime

newid = itertools.count()

#functions
def create_task():
    date = calendar.get_date()
    date = date.strftime('%d/%m/%y')
    tree.insert(parent='', index='end', iid=next(newid), text=task_ent.get(), values=(date))
    task_ent.delete(0, 'end') 

def remove_task(*args):
    selected = tree.selection()
    for task in selected:
        tree.delete(task)

def remove_all():
    selected = tree.get_children()
    for task in selected:
        tree.delete(task)

#Reading and writing data
def write_data():
    selected = tree.get_children()
    with open('tree_data.csv', 'w', newline='') as file:
        fieldnames = ['task', 'due_date']
        dict_writer = csv.DictWriter(file, fieldnames=fieldnames)
        dict_writer.writeheader()
        for t in selected:
            dict_writer.writerow({'task':tree.item(t)['text'], 'due_date':tree.item(t)['values'][0]})
    window.destroy()
        
def get_data():
    try:
        with open('tree_data.csv', 'r', newline='') as file:
            dict_reader = csv.DictReader(file)
            insert_into_tree(dict_reader)
            tree.tag_configure('red', background='red', foreground='white')
            tree.tag_configure('yellow', background='yellow')


    except FileNotFoundError:
        pass

def insert_into_tree(items):
    today = datetime.now().date()
    for t in items:
        task_date = datetime.strptime(t['due_date'], '%d/%m/%y').date()
        delta = task_date - today
        if today >= task_date:
            tree.insert(parent='', index='end', iid=next(newid), text=t['task'], values=(t['due_date']), tags='red')
        elif delta.days > 0 and delta.days <= 3:
            tree.insert(parent='', index='end', iid=next(newid), text=t['task'], values=(t['due_date']), tags='yellow')  
        else:
            tree.insert(parent='', index='end', iid=next(newid), text=t['task'], values=(t['due_date']))

    

def sort_by_date(event):
    sort_by = sort_combo.get()
    task_list = []
    selected = tree.get_children()
    for t in selected:
        task_list.append({'task':tree.item(t)['text'], 'due_date':tree.item(t)['values'][0]})
    remove_all()
    if sort_by == 'Due First':
        task_list.sort(key=lambda x: datetime.strptime(x['due_date'], '%d/%m/%y'))
    else:
        task_list.sort(key=lambda x: datetime.strptime(x['due_date'], '%d/%m/%y'), reverse=True)
    insert_into_tree(task_list)
    tree.tag_configure('red', background='red', foreground='white')
    tree.tag_configure('yellow', background='yellow')

#window
window = tk.Tk()
window.resizable(height=False, width=False)
window.geometry("600x550")

#Frames
north_frame = tk.Frame(master=window)
south_frame = tk.Frame(master=window)

#Widgets
#combobox
sort_combo = ttk.Combobox(north_frame, values=('Due First', 'Due Last'))
sort_combo.set('Sort By: ')

#Tree and Scrollbar
tree = ttk.Treeview(master=north_frame, columns=( 'due_date'))
scroll = ttk.Scrollbar(north_frame, orient='vertical', command=tree.yview)
tree.configure(yscrollcommand=scroll.set)
#scroll config
#column 1 (Task)
tree.column('#0', anchor='center')
tree.heading('#0', text='Task')
#column 2 (Task)
tree.column('due_date', anchor='center')
tree.heading('due_date', text='Due Date')

#labels
task_label = tk.Label(text="Task:", master=south_frame)
due_date_label = tk.Label(text="Due Date:", master=south_frame)

#Buttons
create_task_btn = tk.Button(text="Create Task", master=south_frame, command=create_task)
remove_task_btn = tk.Button(south_frame, text='Remove Task', command=remove_task)
#entrys
task_ent = tk.Entry(width=50, master=south_frame)
calendar = DateEntry(south_frame, date_pattern='dd/mm/yy')


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
create_task_btn.grid(row=2, column=0, padx=5, pady=5)
remove_task_btn.grid(row=2, column=1, padx=5, pady=5)
calendar.grid(row=1, column=1)


#bindings
sort_combo.bind('<<ComboboxSelected>>', sort_by_date)
window.bind('<Delete>', remove_task)
window.after_idle(get_data)
window.protocol("WM_DELETE_WINDOW", write_data)
window.mainloop()


