from tests import TestCase


class TestCommandsAssertions(TestCase):
    def test_running_command_during_tests(self):
        self.craft("help")

    def test_assert_output(self):
        self.craft("help").assertOutputContains("Masonite Version: version 4.0")

    def test_assert_output_missing(self):
        self.craft("help").assertOutputMissing("This is not in the help")

    def test_assert_errors(self):
        with self.assertRaises(AssertionError):
            self.craft("help").assertHasErrors()

    def test_assert_success(self):
        self.craft("help").assertSuccess()
