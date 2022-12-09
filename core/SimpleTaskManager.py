import tkinter as tk
import tkinter.ttk as ttk
from Task import Task
import itertools

newid = itertools.count()

#functions
def create_task():
    tree.insert(parent='', index='end', iid=next(newid), text=task_ent.get(), values=(due_date_ent.get()))

#window
window = tk.Tk()
window.resizable(height=False, width=False)
window.geometry("600x400")

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
task_label = tk.Label(text="Task", master=south_frame)
due_date_label = tk.Label(text="Due Date", master=south_frame)

#Buttons
create_task_btn = tk.Button(text="Create Task", master=south_frame, command=create_task)

#entrys
task_ent = tk.Entry(width=50, master=south_frame)
due_date_ent = tk.Entry(width=30, master=south_frame)


#Adding frames to window
north_frame.pack()
south_frame.pack()

#Adding widgets to frames
tree.grid(row=0,column=0)
scroll.grid(row=0, column=1, sticky='ns')
task_label.grid(row=0, column=0, padx=5, pady=3)
due_date_label.grid(row=0, column=1, padx=5, pady=3)
task_ent.grid(row=1, column=0, padx=5, pady=5)
due_date_ent.grid(row=1, column=1, padx=5, pady=5)
create_task_btn.grid(row=2, column=0, padx=5, pady=5)


#bindings
# create_task_btn.bind("<Button-1>", create_task)


window.mainloop()


