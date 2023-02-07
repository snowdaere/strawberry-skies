# import libraries
import numpy as np
from pygame import gfxdraw as draw
import pygame as g
import math
# import game variables
from GameState import GameState
import Rendering.Colors as Colors
from Entities.Entity import Entity



def drawcircle(surface, pos, r, color):
    '''draw antialized circle at a position on the surface'''
    pos = np.int64(pos)
    draw.filled_circle(surface, *pos, int(r), color)
    draw.aacircle(surface, *pos, int(r), color)

class Center:
    '''an anchor for the central position in a solar system'''
    pos = np.array((0, 0))
    mass = 0

class Sattelite(Entity):
    '''a body, orbits a body or sattelite'''
    def __init__(self, parent, distance:float, mass:float, data:dict) -> None:
        if parent == Center:
            pass
        elif type(parent) == Sattelite:
            pass
        else:
            raise Exception('Sattelite Parent must be a Center or another Sattelite')
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

        if self.distance == 0:
            self.omega = 0
        else:
            self.omega = (1/distance)*(math.sqrt(GameState.G * (self.mass + self.parent.mass))/math.sqrt(self.distance))

        self.color = data['color']
        self.name = data['name']
        self.widename = f' {self.name.upper()} '
        self.renderpos = GameState.Camera.world2render(self.pos)
        self.rendersize = int(GameState.Camera.camzoom*(self.radius))

    
    def label(self):
        '''labels the object in the world; for hud rendering'''
        GameState.display.blit(GameState.font.render(self.widename, True, Colors.black, Colors.white), self.renderpos)
        g.draw.circle(GameState.display, Colors.black, self.renderpos, 2)

    def update(self):
        '''updates state of the sattelite'''
        # Calculate new position
        self.pos = self.parent.pos + self.distance*np.array((np.cos(self.omega*GameState.t), np.sin(self.omega*GameState.t)))
        self.vel = self.distance*self.omega*np.array((-1*np.sin(self.omega*GameState.t), np.cos(self.omega*GameState.t)))

    def render(self):
        '''render sattelite to a display'''
        # get new render info
        self.renderpos = GameState.Camera.world2render(self.pos)
        x, y = self.renderpos
        # radius to be drawn on the screen
        self.rendersize = int(GameState.Camera.camzoom*(self.radius))

        # render the orbit
        #draw.aacircle(display, *np.int64(world2render(self.parent.pos)), int(Camera.camzoom*self.distance), Colors.white)
        g.draw.circle(GameState.display, Colors.white, GameState.Camera.world2render(self.parent.pos), GameState.Camera.camzoom*self.distance, width=1)
        
        # render the planet itself, except if off screen
        if self.rendersize > 2:
            if 0-self.rendersize <= x <= GameState.Camera.width + self.rendersize:
                if 0-self.rendersize <= y <= GameState.Camera.height + self.rendersize:
                    drawcircle(GameState.display, self.renderpos, self.rendersize, self.color)