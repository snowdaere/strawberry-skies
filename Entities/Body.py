# import libraries
import numpy as np
import math
# import game variables
import Rendering.Camera as Camera
import Rendering.Render as Render


class Body:
    '''non moving body; ie a central star. Required to anchor a system'''
    def __init__(self, pos: np.ndarray, mass, data) -> None:
        # position in the game world
        self.pos = pos
        self.vel = np.array((0, 0))
        # mass (for physics)
        self.mass = mass
        # radius of planet
        self.radius = math.atan(self.mass)

        # orbit brackets
        self.minorbit = self.radius * 1.5
        self.maxorbit = self.radius * 2


        self.color = data['color']
        self.name = data['name']
        
    def render(self, display):
        '''render in-world position on screen'''
        rendersize = Camera.camzoom*(self.radius)
        Render.drawcircle(display, Camera.world2render(self.pos), rendersize, self.color)

    def update(self, t):
        '''does nothing'''
        pass