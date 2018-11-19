
class BaseComponent:

    def __init__(self, parent_entity, active=True):
        self.parent_entity = parent_entity
        self.active = active

    def enable(self):
        self.active = True

    def disable(self):
        self.active = False
