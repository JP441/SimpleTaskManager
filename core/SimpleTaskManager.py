import tkinter as tk
import tkinter.ttk as ttk
from Task import Task
import itertools
import csv
from tkcalendar import DateEntry

newid = itertools.count()

#functions
def create_task():
    date = calendar.get_date()
    date = date.strftime('%d/%m/%y')
    tree.insert(parent='', index='end', iid=next(newid), text=task_ent.get(), values=(date))
    task_ent.delete(0, 'end') 

def remove_task():
    selected = tree.selection()
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
            for t in dict_reader:
                tree.insert(parent='', index='end', iid=next(newid), text=t['task'], values=(t['due_date']))
    except FileNotFoundError:
        pass

def sort_by_date():
    selected = tree.get_children()
    task_list = []
    for t in selected:
        task_list.append({'task':tree.item(t)['text'], 'due_date':tree.item(t)['values'][0]})
    print(task_list)


#window
window = tk.Tk()
window.resizable(height=False, width=False)
window.geometry("600x550")

#Frames
north_frame = tk.Frame(master=window)
south_frame = tk.Frame(master=window)

#Widgets
#Scrollbar
#Tree
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
sort_btn = tk.Button(south_frame, command=sort_by_date, text='sort')
#entrys
task_ent = tk.Entry(width=50, master=south_frame)
calendar = DateEntry(south_frame, date_pattern='dd/mm/yy')


#Adding frames to window
north_frame.pack()
south_frame.pack()

#Adding widgets to frames
tree.grid(row=0,column=0)
scroll.grid(row=0, column=1, sticky='ns')
task_label.grid(row=0, column=0, pady=3,)
due_date_label.grid(row=1, column=0, pady=3)
task_ent.grid(row=0, column=1, pady=5)
create_task_btn.grid(row=2, column=0, padx=5, pady=5)
remove_task_btn.grid(row=2, column=1, padx=5, pady=5)
calendar.grid(row=1, column=1)
sort_btn.grid(row=3, column=0)


#bindings
# create_task_btn.bind("<Button-1>", create_task)
window.after_idle(get_data)
window.protocol("WM_DELETE_WINDOW", write_data)
window.mainloop()


