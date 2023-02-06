import numpy as np
import pygame as g

from GameState import GameState
from Entities.Entity import Entity

class Freebody(Entity):
    '''this is an object defined by accelerating freely due to gravity'''
    def __init__(self, x:float, y:float, color):
        # physics variables
        self.pos = np.array((x, y))
        self.vel = np.array((0.0, 0.0))
        self.acc = np.array((0.0, 0.0))
        self.color = color

        self.mass = 0.01

        # gameplay information
        self.dead = False
        self.distances = [0.0] * len(GameState.Bodies)

        self.size = 0.01
        self.rendersize = int(GameState.Camera.camzoom*(self.size))

    def getdistfrom(self, object):
        '''get distance between the ship and an object'''
        dx = self.pos[0] - object.pos[0]
        dy = self.pos[1] - object.pos[1]
        return np.sqrt(dx**2 + dy**2)

    def updatedist(self):
        '''updates the distances from the ship to each body'''
        for i, object in enumerate(GameState.Bodies):
            self.distances[i] = self.getdistfrom(object)

    def getunit(self, object):
        '''returns unit vector pointing at the object'''
        return (self.pos-object.pos)/self.getdistfrom(object)

    def updateaccel(self):
        '''updates acceleration according to the distances to bodies'''
        acc = np.array((0, 0))
        for i, r in enumerate(self.distances):
            body = GameState.Bodies[i]
            acc  = acc -1*GameState.G*body.mass*(1/r**2)*self.getunit(body)
        self.acc = acc


    def update(self):
        '''update the player state and location and information'''
        ### NOTE I have turned collision off for these objects; theyre for a stress test

        # update distances
        self.updatedist()

        # calculate acceleration
        self.updateaccel()

        # here, if the ship is not orbiting anything
        ### NOTE use verlet integration for this you fool
        self.vel = self.vel + (GameState.dt * self.acc)
        self.pos = self.pos + (GameState.dt * self.vel)
                

    def render(self):
        '''render the object'''
        # DEFAULT IS 0.01
        # update rendersize
        # self.rendersize = int(Camera.camzoom*(self.size))
        self.rendersize = 10
        renderpos = GameState.Camera.world2render(self.pos)

        # draw dot at ship position itself
        g.draw.circle(GameState.display, self.color, renderpos, self.rendersize)
