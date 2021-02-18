""" Event Module """

from .exceptions import InvalidSubscriptionType


class Event:
    def __init__(self, application):
        """Event contructor
        Arguments:
            application - The Masonite application class
        """
        self.application = application
        self.listeners = {}
        self._fired_events = {}
        self._arguments = {}

    def event(self, event):
        """Starts the event observer
        Arguments:
            event {string|object}
        """

        self.listen(event, [])

    def listen(self, event, listeners=[]):
        """Add a listener to an event.
        Arguments:
            event {string|object} -- [description]
        Keyword Arguments:
            listeners {list} -- A list of listner classes that should listen to specific events (default: {[]})
        Returns:
            self
        """

        if event in self.listeners:
            self.listeners[event] += listeners
            return self

        self.listeners.update({event: listeners})
        return self

    def fire(self, events, **keywords):
        """Fire an event which fires all the listeners attached to that event.
        Arguments:
            events {string|object} -- The event to fire
        """

        fired_listeners = {}
        if isinstance(events, str) and "*" in events:
            for event_action, listener_events in self.listeners.items():
                fired_listeners.update({event_action: []})
                for listener in listener_events:
                    search = events.split("*")
                    if (
                        events.endswith("*")
                        and event_action.startswith(search[0])
                        or events.startswith("*")
                        and event_action.endswith(search[1])
                        or event_action.startswith(search[0])
                        and event_action.endswith(search[1])
                    ):
                        event = self.container.resolve(listener)
                        fired_listeners[event_action].append(event)
                        for key, value in keywords.items():
                            event._arguments.update({key: value})
                        self.container.resolve(event.handle)
        else:
            fired_listeners.update({events: []})
            for event in self.listeners[events]:
                event = self.container.resolve(event)
                fired_listeners[events].append(event)
                for key, value in keywords.items():
                    event._arguments.update({key: value})
                self.container.resolve(event.handle)

        self._fired_events = self.clear_blank_fired_events(fired_listeners)

    def clear_blank_fired_events(self, fired_listeners):
        """Just an internal cleaner helper that cleans any the listeners for any fired events.
        This will, in effect, return the fired events
        Arguments:
            fired_listeners {dict} -- dictionary of event and listeners
        Returns:
            dict -- returns a dictionary of fired events
        """

        new_dictionary = {}
        for event, listeners in fired_listeners.items():
            if listeners:
                new_dictionary.update({event: listeners})

        return new_dictionary

    def subscribe(self, *listeners):
        """Subscribe a specific listener object to the events system
        Raises:
            InvalidSubscriptionType -- raises when the subscribe attribute on the listener object is not a class.
        """

        for listener in listeners:
            if not isinstance(listener.subscribe, list):
                raise InvalidSubscriptionType(
                    "'subscribe' attribute on {0} class must be a list".format(
                        listener.__name__
                    )
                )
            for action in listener.subscribe:
                self.listen(action, [listener])

    def argument(self, argument):
        """Takes the argument and eventually stores the argument on the event class
        Arguments:
            argument {string|obj|list|dict} -- Any data type that can be a class attribute
        Returns:
            dict
        """

        return self._arguments[argument]
