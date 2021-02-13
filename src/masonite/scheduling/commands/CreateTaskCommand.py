""" A CreateTask Command """
import os

from cleo import Command


class CreateTaskCommand(Command):
    """
    Create a new task
    task
        {name : Name of the task you want to create}
    """

    def handle(self):
        task = self.argument("name")
        if not os.path.isfile("app/tasks/{0}.py".format(task)):
            if not os.path.exists(os.path.dirname("app/tasks/{0}.py".format(task))):
                # Create the path to the Task if it does not exist
                os.makedirs(os.path.dirname("app/tasks/{0}.py".format(task)))

            f = open("app/tasks/{0}.py".format(task), "w+")

            f.write("''' Task Module Description '''\n")
            f.write("from masonite.scheduler.Task import Task\n\n")
            f.write(
                "class {0}(Task):\n    ''' Task description '''\n\n    ".format(task)
            )
            f.write("def __init__(self):\n        pass\n\n    ")
            f.write("def handle(self):\n        pass\n")

            self.info("Task Created Successfully!")
        else:
            self.error("Task Already Exists!")
