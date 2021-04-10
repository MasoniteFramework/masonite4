from .NotificationManager import NotificationManager
from .AnonymousNotifiable import AnonymousNotifiable


class MockNotification(NotificationManager):
    def __init__(self, application, *args, **kwargs):
        super().__init__(application, *args, **kwargs)
        self.count = 0

    def send(
        self, notifiables, notification, drivers=[], dry=False, fail_silently=False
    ):
        _notifiables = []
        for notifiable in self._format_notifiables(notifiables):
            if isinstance(notifiable, AnonymousNotifiable):
                _notifiables.extend(notifiable._routes.values())
            else:
                _notifiables.append(notifiable)
        key = notification.type()
        # store notifications instead of sending them
        old_notifiables = self.sent_notifications.get(key, [])
        self.sent_notifications.update({key: old_notifiables + _notifiables})
        self.count += len(_notifiables)
        return self

    def resetCount(self):
        """Reset sent notifications count."""
        self.count = 0
        self.sent_notifications = {}
        return self

    def assertNothingSent(self):
        assert self.count == 0, f"{self.count} notifications have been sent."
        # assert len(self.sent_notifications.keys()) == 0
        return self

    def assertCount(self, count):
        assert (
            self.count == count
        ), f"{self.count} notifications have been sent, not {count}."
        return self

    def assertSentTo(self, notifiable, notification_class, count=None):
        from collections import Counter

        notifiables = self.sent_notifications.get(notification_class.__name__, [])
        assert notifiable in notifiables
        if count:
            counter = Counter(notifiables)
            assert counter[notifiable] == count
        return self

    def assertNotSentTo(self, notifiable, notification_class):
        notifiables = self.sent_notifications.get(notification_class.__name__, [])
        assert notifiable not in notifiables
        return self
