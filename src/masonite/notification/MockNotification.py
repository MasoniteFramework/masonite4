from .NotificationManager import NotificationManager


class MockNotification(NotificationManager):
    def __init__(self, application, *args, **kwargs):
        super().__init__(application, *args, **kwargs)
        self.count = 0

    def send(
        self, notifiables, notification, drivers=[], dry=False, fail_silently=False
    ):
        self.called_notifications.append(notification)
        return self
