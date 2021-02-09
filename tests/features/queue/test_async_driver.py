from tests import TestCase
from src.masonite.queues import Queueable
import os
import time


class SayHello(Queueable):
    def handle(self):
        print("hello there")


class TestAsyncDriver(TestCase):
    def test_async_push(self):
        self.application.make("queue").push(SayHello())
