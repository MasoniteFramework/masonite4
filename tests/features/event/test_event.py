import time

import pytest

from src.masonite.events import Event
from src.masonite.events.exceptions import InvalidSubscriptionType
from tests import TestCase


class UserAddedEvent(Event):
    subscribe = []

    def __init__(self):
        pass

    def handle(self):
        pass


class SomeAction:
    pass


class EventListener:
    def handle(self):
        pass


class EventWithSubscriber(Event):

    subscribe = ["user.registered"]

    def __init__(self):
        pass

    def handle(self):
        pass


class TestEvent(TestCase):
    def setUp(self):
        super().setUp()
        self.event = self.application.make("event")

    def test_fire_event_with_wildcard_ends_with(self):
        events = self.event.listen("user.registered", [EventListener, EventListener])

        # events = self.app.make('Event').listen('user.subscribed', [
        #     EventListener
        # ])

        # event = self.app.make('Event')

        # assert event.fire('*.registered') is None
        # assert isinstance(
        #     event._fired_events['user.registered'][0], EventListener)

    # def test_add_listener(self):
    #     self.app.make('Event').listeners = {}
    #     events = self.app.make('Event').listen(UserAddedEvent, [
    #         EventListener
    #     ])

    #     assert events.listeners == {UserAddedEvent: [EventListener]}

    #     events.listen(UserAddedEvent, [EventListener])

    #     assert events.listeners == {
    #         UserAddedEvent: [EventListener, EventListener]}

    # def test_fire_event(self):
    #     events = self.app.make('Event').listen(UserAddedEvent, [
    #         EventListener
    #     ])

    #     assert events.fire(UserAddedEvent) is None
    #     assert isinstance(
    #         events._fired_events[UserAddedEvent][0], EventListener)

    # def test_fire_event_with_wildcard_starts_with(self):
    #     self.app.make('Event').listeners = {}
    #     events = self.app.make('Event').listen('user.registered', [
    #         EventListener
    #     ])
    #     events = self.app.make('Event').listen('user.subscribed', [
    #         EventListener
    #     ])

    #     event = self.app.make('Event')

    #     assert event.fire('user.*') is None
    #     assert isinstance(
    #         event._fired_events['user.registered'][0], EventListener)
    #     assert isinstance(
    #         event._fired_events['user.subscribed'][0], EventListener)

    # def test_fire_event_with_wildcard_in_middle_of_fired_event(self):
    #     self.app.make('Event').listeners = {}
    #     events = self.app.make('Event').listen('user.manager.registered', [
    #         EventListener
    #     ])
    #     events = self.app.make('Event').listen('user.owner.subscribed', [
    #         EventListener
    #     ])

    #     event = self.app.make('Event')

    #     assert event.fire('user.*.registered') is None
    #     assert isinstance(
    #         event._fired_events['user.manager.registered'][0], EventListener)

    # def test_event_subscribers(self):
    #     self.app.make('Event').listeners = {}
    #     events = self.app.make('Event').subscribe(EventWithSubscriber)

    #     assert self.app.make('Event').listeners == {
    #         'user.registered': [EventWithSubscriber]}

    # def test_event_with_multiple_subscribers(self):
    #     self.app.make('Event').listeners = {}
    #     event = EventWithSubscriber

    #     event.subscribe = ['user.registered', 'user.subscribed']

    #     self.app.make('Event').subscribe(event)

    #     assert self.app.make('Event').listeners == {'user.registered': [
    #         EventWithSubscriber], 'user.subscribed': [EventWithSubscriber]}

    # def test_event_with_throws_exception_with_invalid_subscribe_attribute_type(self):
    #     self.app.make('Event').listeners = {}
    #     event = EventWithSubscriber

    #     event.subscribe = 'user.registered'

    #     with pytest.raises(InvalidSubscriptionType):
    #         self.app.make('Event').subscribe(event)

    # def test_event_starts_event_observer(self):
    #     self.app.make('Event').listeners = {}
    #     self.app.make('Event').event('user.subscribed')
    #     assert self.app.make('Event').listeners == {'user.subscribed': []}

    # def test_event_sets_keyword_arguments(self):
    #     self.app.make('Event').listeners = {}
    #     event = EventWithSubscriber

    #     event.subscribe = ['user.registered', SomeAction]

    #     self.app.make('Event').subscribe(event)

    #     self.app.make('Event').fire('user.registered', to='user@email.com')
    #     assert self.app.make('Event')._fired_events['user.registered'][0].argument(
    #         'to') == 'user@email.com'

    #     self.app.make('Event').fire(SomeAction, to='test@email.com')

    #     assert self.app.make('Event')._fired_events[SomeAction][0].argument(
    #         'to') == 'test@email.com'
