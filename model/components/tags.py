from model.components.base_component import BaseComponent

#many components don't need their own class file, and are instead just tags that signify
#yes or no characteristics.  I will put those here and call them "tags".

class CanOpenDoors(BaseComponent):
    pass

class ObstructsMovement(BaseComponent):
    pass
