class Task:
    def __init__(self, task, due_date=None):
        self.task = task
        self.due_date = due_date
    
    def get_task(self):
        return self.task
    
    def get_due_date(self):
        return self.due_date

    def set_task(self, x):
        self.task = x

    def set_due_date(self, x):
        self.due_date = x