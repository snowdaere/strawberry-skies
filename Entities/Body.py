# import libraries
import numpy as np
from pygame import gfxdraw as draw
import math
# import game variables
import Rendering.Camera as Camera


def drawcircle(surface, pos, r, color):
    pos = np.int64(pos)
    draw.filled_circle(surface, *pos, int(r), color)
    draw.aacircle(surface, *pos, int(r), color)


class Body:
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
        # radius to be drawn on the screen
        rendersize = Camera.camzoom*(self.radius)
        drawcircle(display, Camera.world2render(self.pos), rendersize, self.color)

    def update(self, t):
        pass