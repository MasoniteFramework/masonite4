from tests import TestCase


class TestApplication(TestCase):
    def test_is_running_tests(self):
        import pdb

        pdb.set_trace()
        self.assertTrue(self.application.is_running_tests())
