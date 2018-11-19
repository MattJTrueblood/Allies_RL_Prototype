

class Entity:

    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
        self.components = []

    def get_component(self, component_type):
        return next((component for component in self.components if isinstance(component, component_type) and component.active), None)

    def get_component_including_disabled(self, component_type):
        return next((component for component in self.components if isinstance(component, component_type)), None)

    def add_component(self, component):
        if not self.get_component(type(component)):
            self.components.append(component)
