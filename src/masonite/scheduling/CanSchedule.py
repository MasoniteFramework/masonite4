class CanSchedule:
    def call(self, command):
        command_class = CommandTask(command)
        self.app.simple(command_class)
        return command_class

    def schedule(self, task):
        task_class = task
        self.app.simple(task_class)
        return task_class
