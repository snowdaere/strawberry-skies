# import libraries
import numpy as np
from pygame import gfxdraw as draw
import pygame as g
import math
# import game variables
import GameState
import Rendering.Camera as Camera
import Rendering.Colors as Colors
# import other classes
import Entities.Body as Body


def drawcircle(surface, pos, r, color):
    '''draw antialized circle at a position on the surface'''
    pos = np.int64(pos)
    draw.filled_circle(surface, *pos, int(r), color)
    draw.aacircle(surface, *pos, int(r), color)


class Sattelite:
    '''a body, orbits a body or sattelite'''
    def __init__(self, parent:Body.Body, distance:float, mass:float, data:dict) -> None:
        self.parent = parent
        self.distance = distance

        # mass (for physics)
        self.mass = mass
        # radius of planet
        self.radius = math.atan(self.mass)

        # orbit brackets
        self.minorbit = self.radius * 1.5
        self.maxorbit = self.radius * 2


        # position in the game world
        ### NOTE in the future make this pick a random position along the circle to render
        self.pos = self.parent.pos + np.array((self.distance, 0))
        self.vel = np.array((0, 0))

        self.omega = (1/distance)*(math.sqrt(GameState.G * (self.mass + self.parent.mass))/math.sqrt(self.distance))

        self.color = data['color']
        self.name = data['name']


    def update(self, t):
        '''updates state of the sattelite'''
        # Calculate new position
        self.pos = self.parent.pos + self.distance*np.array((np.cos(self.omega*t), np.sin(self.omega*t)))
        self.vel = self.distance*self.omega*np.array((-1*np.sin(self.omega*t), np.cos(self.omega*t)))


    def render(self, display):
        '''render sattelite to a display'''
        # radius to be drawn on the screen
        rendersize = int(Camera.camzoom*(self.radius))

        # render the orbit
        #draw.aacircle(display, *np.int64(world2render(self.parent.pos)), int(Camera.camzoom*self.distance), Colors.white)
        g.draw.circle(display, Colors.white, Camera.world2render(self.parent.pos), Camera.camzoom*self.distance, width=1)
        
        # render the planet itself
        drawcircle(display, Camera.world2render(self.pos), rendersize, self.color)