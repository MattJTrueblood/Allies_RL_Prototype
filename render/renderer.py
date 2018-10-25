import core
import tcod

#Globals
render_frames = []
current_frame = None

def render():
    if current_frame:
        #print("render is go!")
        current_frame.render()
    tcod.console_flush()

def add_frame(new_frame):
    render_frames.append(new_frame)

def set_current_frame(frame_name):
    global current_frame
    current_frame = next((x for x in render_frames if x.name == frame_name), None)
