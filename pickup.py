PICKUP_NAMES = {
    "jumping_power": "Jumping Power",
    "double_jump": "Double Jump",
    "trampoline": "Trampoline",
    "no_hurry": "No Hurry",
    "double_points": "Double Points"
}
class Pickup:
    def __init__(self, pickup_type, duration):
        self.pickup_type = pickup_type
        self.duration = duration

    def update(self, dt):
        self.duration -= dt

    def alive(self):
        return self.duration > 0
