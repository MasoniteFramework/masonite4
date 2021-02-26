from tests import TestCase
import os
import time
from src.masonite.broadcasting import Channel, PrivateChannel


class CanBroadcast:
    def broadcast_on(self):
        return PrivateChannel(f"order.{self.order_id}")

    def broadcast_with(self):
        return vars(self)

    def broadcast_as(self):
        return self.__class__.__name__


class OrderProcessed(CanBroadcast):
    def __init__(self):
        self.order_id = 1


class TestFileCache(TestCase):
    def setUp(self):
        super().setUp()
        self.application.make("cache")
        self.driver = self.application.make("broadcast")

    # def test_can_get_file_driver(self):
    #     print(self.driver.channel('order.1', 'status', {"status": "processed"}))

    def test_can_fire_class(self):
        print(self.driver.channel("private-orders", OrderProcessed()))
