import numpy as np
import Camera
import GameState
import Colors
import pygame as g
import System1

Bodies = System1.System

class Player:
    '''the player object'''
    def __init__(self, x:float, y:float, color):
        # physics variables
        self.pos = np.array((x, y))
        self.vel = np.array((0.0, 0.0))
        self.acc = np.array((0.0, 0.0))
        self.color = color

        self.mass = 0.01

        #self.theta = np.arctan(self.vel[1]/self.vel[0])

        # gameplay information
        self.dead = False


        # orbit information
        self.orbiting = False
        # position relative to nearby planet
        self.orbitinit = np.array((0, 0))
        self.orbit = None


        self.nearestdist = 0
        self.nearest = None
        self.nearestinit = np.array((0, 0))

        self.selectionhold = False
        self.selecteddist = 0
        self.selected = None

        self.distances = [0.0] * len(Bodies)


        # play information
        self.thrusting = False
        self.thrustforce = 0.005


    def getdistfrom(self, object):
        '''get distance between the ship and an object'''
        dx = self.pos[0] - object.pos[0]
        dy = self.pos[1] - object.pos[1]
        return np.sqrt(dx**2 + dy**2)

    def updatedist(self, bodies):
        '''updates the distances from the ship to each body'''
        for i, object in enumerate(bodies):
            self.distances[i] = self.getdistfrom(object)

    def getunit(self, object):
        '''returns unit vector pointing at the object'''
        return (self.pos-object.pos)/self.getdistfrom(object)

    def thrust(self):
        '''applies thrust to the ship according to its mass'''
        mousepos = Camera.render2world(g.mouse.get_pos())
        dif = self.pos-mousepos
        unit = (dif)/np.sqrt(dif[0]**2 + dif[1]**2)
        self.thrusting = True
        return unit*(self.thrustforce/self.mass)

    def updateaccel(self, bodies):
        '''updates acceleration according to the distances to bodies'''
        acc = np.array((0, 0))
        for i, r in enumerate(self.distances):
            body = bodies[i]
            acc  = acc -1*GameState.G*body.mass*(1/r**2)*self.getunit(body)
        if self.thrusting:
            acc -= self.thrust()
        self.acc = acc

    def setnearest(self, bodies):
        '''picks out which object is nearest (for selection)'''
        min = 10000
        mindex = -1
        # find minimim object
        for i, dist in enumerate(self.distances):
            if dist < min:
                min = dist
                mindex = i
        # set variables based on findings
        self.nearest = bodies[mindex]
        self.nearestdist = min
        self.nearestinit = self.pos - self.nearest.pos

        # do selection logic, depengin
        if self.selectionhold:        
            self.selecteddist = self.nearestdist
        if not self.selectionhold:
            self.selected = self.nearest

    def attemptorbit(self):
        '''attempts to orbit the selected body'''
        # attempt to orbit the nearest body if within bracket
        ### TODO make it so that you must approach within 45 degrees of the orbital face to engage orbit
        ### and change the orbit bracket colors to match 
        if self.selected.minorbit <= self.selecteddist <= self.selected.maxorbit:
            self.orbiting = True
            self.orbit = self.selected
            self.orbitinit = self.nearestinit
    
    def deorbit(self):
        '''pulls you out of orbit'''
        ### TODO actually make a proper 
        self.orbiting = False

    def respawn(self):
        '''respawns your ship off world'''
        ### TODO Make it place you in orbit
        if self.dead:
            self.dead = False
            # place you in orbital bracket behind planet
            self.pos = self.nearest.pos + 2*self.nearest.radius
            self.vel = self.nearest.vel


    def update(self):
        '''update the player state and location and information'''
        if not self.dead:
            if not self.orbiting:
                # update distances
                self.updatedist(Bodies)

                # find nearest planet
                self.setnearest(Bodies)

                # calculate acceleration
                self.updateaccel(Bodies)

                # here, if the ship is not orbiting anything
                ### NOTE use verlet integration for this you fool
                self.vel = self.vel + (GameState.dt * self.acc)
                self.pos = self.pos + (GameState.dt * self.vel)
                
            else:
                # here, movement if the ship is orbiting something
                self.pos = self.orbit.pos + self.orbitinit
                self.vel = self.orbit.vel

        # check if you are dead
        if self.nearestdist <= self.nearest.radius:
            self.dead = True
            self.pos = self.nearest.pos + self.nearestinit


    def render(self, display):
        '''render the Player and its HUD'''
        # DEFAULT IS 0.01
        rendersize = int(Camera.camzoom*(0.01))

        # draw ship itself
        g.draw.circle(display, self.color, Camera.world2render(self.pos), rendersize)