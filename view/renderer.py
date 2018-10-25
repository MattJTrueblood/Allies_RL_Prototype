import core
import tcod

def render():
    if core.current_frame:
        core.current_frame.render()
    tcod.console_flush()
