from tests import TestCase


class TestCommandsAssertions(TestCase):
    def test_running_command_during_tests(self):
        self.craft("key")

    def test_assert_output(self):
        self.craft("key").assertOutputContains("Key added to your .env file:")

        # this command prints also key value
        with self.assertRaises(AssertionError):
            self.craft("key").assertExactOutput("Key added to your .env file:")

    def test_assert_output_missing(self):
        self.craft("key").assertOutputMissing("This is not in output")

    def test_assert_errors(self):
        # this commands has no errors
        with self.assertRaises(AssertionError):
            self.craft("key").assertHasErrors()

    def test_assert_success(self):
        self.craft("key").assertSuccess()
