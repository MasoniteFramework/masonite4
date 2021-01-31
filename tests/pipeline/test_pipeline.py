from src.masonite.tests import TestCase
from src.masonite.pipeline import Pipeline
from src.masonite.request import Request
import os


class PipeTestOne:
    def handle(self, request):
        request.one = 1

        return request


class PipeTestTwo:
    def handle(self, request):
        request.two = 2

        return request


class PipeTestBreak:
    def handle(self, request):
        return False


class PipeTestThree:
    def handle(self, request):
        request.three = 3

        return request


class TestPipeline(TestCase):
    def test_pipeline_sets_attributes(self):
        request = Request()
        pipeline = Pipeline(request).through([PipeTestOne, PipeTestTwo])
        self.assertTrue(request.one == 1)
        self.assertTrue(request.two == 2)

    def test_pipeline_exits(self):
        request = Request()
        pipeline = Pipeline(request).through([PipeTestOne, PipeTestBreak])
        self.assertTrue(request.one == 1)
        with self.assertRaises(AttributeError):
            self.assertTrue(request.two == 2)
