class BaseDriver:
    def send(self, notifiable, notification):
        """Implements sending the notification to notifiables through
        this driver."""
        raise NotImplementedError(
            "send() method must be implemented for a notification driver."
        )

    def queue(self, notifiable, notification):
        """Implements queueing the notification to be sent later 
        this driver."""
        raise NotImplementedError(
            "queue() method must be implemented for a notification driver."
        )

    def get_data(self, driver, notifiable, notification):
        """Get the data for the notification."""
        method_name = f"to_{driver}"
        try:
            method = getattr(notification, method_name)
        except AttributeError:
            raise NotImplementedError(
                "Notification model should implement {}() method.".format(method_name)
            )
        else:
            return method(notifiable)
