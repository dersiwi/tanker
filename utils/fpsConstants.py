class Globals:
    class CollisionClass:
        NO_COLLISION = 0
        CLASS_ONE = 1
        """
        Collison class One objects cannot be described by a bounding box. Objects of this class can
        only collide with collision class two objects.
        for this they have to implement the collision_detection() method
        """
        CLASS_TWO = 2
        """
        Collision class two objects can be sourrounded by a bounding bog. Collision class two 
        obejcts can collide with other class two objects and with class one objects
        """
        CLASSES = [NO_COLLISION, CLASS_ONE, CLASS_TWO]

    class FPS:
        FPS = 30
        dt = 1 / FPS

        
    SCREEN_WIDTH = int(900)
    SCREEN_HEIGHT = int(600)
    GRAVITY = 300