'''
Created on Jul 7, 2011

@author: anttir
'''

class Event:
    def __init__(self, name='Generic event'):
        self.name=name

class KeyboardEvent(Event):
    def __init__(self, key, up):
        Event.__init__(self, 'Keyboard')
        self.key=key
        self.up=up

class MouseEvent(Event):
    def __init__(self, key, up):
        Event.__init__(self, 'Mouse')
        self.key = key
        self.up = up   

class TickEvent(Event):
    def __init__(self, time):
        Event.__init__(self, 'Tick')
        self.time=time

class ShootEvent(Event):
    def __init__(self,side='mid'):
        Event.__init__(self,'Shoot')
        self.side=side

class PointEvent(Event):
    def __init__(self,points):
        Event.__init__(self,'Point')
        self.points=points
        
class EnemyShootEvent(Event):
    def __init__(self,enemy):
        Event.__init__(self, 'EnemyShoot')
        self.enemy=enemy

class KillEvent(Event):
    def __init__(self,drop,enemy):
        Event.__init__(self, 'kill')
        self.drop=drop
        self.enemy=enemy

class EventManager:
    def __init__(self):
        from weakref import WeakKeyDictionary
        self.listeners = WeakKeyDictionary()
        
    def register(self, listener):
        self.listeners[listener] = 1
        
    def unregister(self, listener):
        del self.listeners[listener]
        
    def tell(self, event):
        if isinstance(event, basestring):
            event = Event(event)
        for listener in self.listeners.keys():
            if listener.notify(event):
                break
