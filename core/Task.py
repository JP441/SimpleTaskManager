import itertools

class Task:
    newid = itertools.count()
    def __init__(self, task, due_date=None):
        self.id = next(Task.newid)
        self.task = task
        self.due_date = due_date

    def get_id(self):
        return self.id
    
    def get_task(self):
        return self.task
    
    def get_due_date(self):
        return self.due_date

    def set_task(self, x):
        self.task = x

    def set_due_date(self, x):
        self.due_date = x

test1 = Task("Take dog for walk", "20-12-22")
test2 = Task("Take dog for walk", "20-12-22")

print(test1.get_id())
print(test2.get_id())