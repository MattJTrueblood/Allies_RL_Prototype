
'''
Frame is a container for Panels.  It contains a render function to render all the panels it contains, and a name to switch between frames as needed.
'''

class Frame:
    def __init__(self, name):
        self.name = name
        self.panels = []

    def render(self):
        for panel in self.panels:
            panel.render()

    def add_panel(self, panel):
        self.panels.append(panel)
