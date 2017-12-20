from nameko.events import EventDispatcher, event_handler
from nameko.rpc import rpc

class ServiceA(object):
    name = 'servicea'
    dispatch = EventDispatcher()

    @rpc
    def emit_an_event(self):
        self.dispatch('my_event_type', 'payload')


class ServiceB(object):
    name = 'serviceb'

    @event_handler('servicea', 'my_event_type')
    def handle_an_event(self, payload):
        print('service b received', payload)
