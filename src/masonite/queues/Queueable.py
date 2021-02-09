"""Base Queue Module."""


class Queueable:
    """Makes classes Queueable."""

    run_again_on_fail = True
    run_times = 3

    def handle(self):
        pass
