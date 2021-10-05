""" A ScheduleProvider Service Provider """
from ...providers import Provider

from ..commands.CreateTaskCommand import CreateTaskCommand
from ..commands.ScheduleRunCommand import ScheduleRunCommand
from ..TaskHandler import TaskHandler


class ScheduleProvider(Provider):
    def __init__(self, application):
        self.application = application

    def register(self):
        self.application.make("commands").add(
            CreateTaskCommand(), ScheduleRunCommand(self.application)
        )

        self.application.bind("scheduler", TaskHandler(self.application))

    def boot(self):
        pass
