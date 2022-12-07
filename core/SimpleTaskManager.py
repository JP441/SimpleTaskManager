import tkinter as tk
import tkinter.ttk as ttk
from Task import Task

task_list = []

window = tk.Tk()
#Frames
north_frame = tk.Frame(master=window)
south_frame = tk.Frame(master=window)



#Widgets
#task_lbl = tk.Label(text="Task:", master=north_frame)
#Buttons
create_task_btn = tk.Button(text="Create Task", master=south_frame)
task_ent = tk.Entry(width=50, master=south_frame)



#Adding widgets to window
north_frame.pack(fill=tk.X)
south_frame.pack()
#task_lbl.grid(row=0, column=0, sticky="w", padx=0, pady=5)
create_task_btn.grid(row=0, column=0, padx=5, pady=5)
task_ent.grid(row=0, column=1, padx=5, pady=5)

def create_task(event):
    task_list.append(Task(task_ent.get()))
    i = 0
    for t in task_list:
        label = tk.Label(master=north_frame, text=task_list[i].get_task())
        label.grid(row=i,column=0)
        i += 1

#bindings
create_task_btn.bind("<Button-1>", create_task)


window.mainloop()


