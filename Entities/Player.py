import numpy as np
import pygame as g

import Rendering.Colors as Colors
from GameState import GameState
from Entities.Freebody import Freebody


class Player(Freebody):
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
        self.distances = [0.0] * len(GameState.Bodies)

        # orbit information
        self.orbiting = False
        # position relative to nearby planet
        self.orbitinit = np.array((0, 0))
        self.orbit = None

        self.nearestdist = 0
        self.nearestinit = np.array((0, 0))
        self.nearest = None

        self.selectionhold = False
        self.selecteddist = 0
        self.selected = None

        ## control information
        self.thrusting = False
        self.thrustforce = 0.0005
        self.thrustdir = 0
        self.rotateCCW = False
        self.rotateCW = False

        self.theta = 0
        self.dtheta = 0.01* GameState.dt * np.pi/self.mass
        
        # rendering information
        self.size = 0.003
        self.rendersize = int(GameState.Camera.camzoom*(self.size))
        self.renderpos = GameState.Camera.world2render(self.pos)
        self.img = g.image.load('Assets/smolrocket.png').convert()
    



        # ship drawing thing; vec0 is the default ship shape, always stored
        # vec is the current orientation
        self.vec0 = (
            np.array((1, 0)),
            np.array((-0.5, 0.5)),
            np.array((-0.5, -0.5))
        )

        self.vec = [
            (1, 0),
            (-0.5, 0.5),
            (-0.5, -0.5)
        ]

        # rotation stuff
        c, s = np.cos(self.theta), np.sin(self.theta)
        self.directionvec = np.array((c, s))
        self.rotatematrix = np.array(((c, -s), (s, c)))

    def thrust(self, dir:int):
        '''applies thrust to the ship according to its mass'''
        # back thrust mechanic
        #return self.directionvec*(self.thrustforce/self.mass)
        rotations = [
            np.array(((1, 0), (0, 1))),
            np.array(((0, -1), (1, 0))),
            np.array(((-1, 0), (0, -1))),
            np.array(((0, 1), (-1, 0)))
        ]
        #self.thrusting = True

        return np.matmul(self.directionvec*(self.thrustforce/self.mass), rotations[dir])


    ### TODO implement rotation
    def rotate(self, d:int):
        '''rotates ship according to mass; 1 is CCW, -1 is CW'''
        # only called when rotating
        # update theta value
        self.theta += d*self.dtheta % (2*np.pi)

        # update rotation math
        c, s = np.cos(self.theta), np.sin(self.theta)
        self.directionvec = np.array((c, s))
        self.rotatematrix = np.array(((c, -s), (s, c)))

        
    def updateaccel(self):
        '''updates acceleration according to the distances to bodies'''
        acc = np.array((0, 0))
        for i, r in enumerate(self.distances):
            body = GameState.Bodies[i]
            acc  = acc -1*GameState.G*body.mass*(1/r**2)*self.getunit(body)
        if self.thrusting:
            acc += self.thrust(self.thrustdir)
        self.acc = acc

    def setnearest(self):
        '''picks out which object is nearest (for selection)'''
        min = 10000
        mindex = -1
        # find minimim object
        for i, dist in enumerate(self.distances):
            if dist < min:
                min = dist
                mindex = i
        # set variables based on findings
        self.nearest = GameState.Bodies[mindex]
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
            # update player orientation
            mousepos = GameState.Camera.render2world(g.mouse.get_pos())
            dif = mousepos-self.pos
            self.directionvec = c, s = (dif)/np.sqrt(dif[0]**2 + dif[1]**2)
            self.rotatematrix = np.array(((c, -s), (s, c)))

            # switch between orbit and free mode
            if not self.orbiting:
                # update distances
                self.updatedist()

                # find nearest planet
                self.setnearest()

                # calculate acceleration
                self.updateaccel()

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


    def render(self):
        '''render the Player and its HUD'''
        # DEFAULT IS 0.01
        # update rendersize
        ### NOTE i am making the arrow appear same size on every zoom level so its easier to read
        #self.rendersize =10 2*int(GameState.Camera.camzoom*(self.size))
        self.rendersize = 5

        self.renderpos = GameState.Camera.world2render(self.pos)

        x, y = self.renderpos


        # draw dot at ship position itself
        if self.rendersize > 2:
            if 0-self.rendersize <= x <= GameState.Camera.width + self.rendersize:
                if 0-self.rendersize <= y <= GameState.Camera.height + self.rendersize:
                    # if zoomed in enough, render the ship
                    # if zoomed out, draw arrow
                    # update drawing vectors
                    # tempvec = map(self.rotatematrix.dot, self.vec0)

                    # split and transform vector
                    for i, v in enumerate(map(self.rotatematrix.dot, self.vec0)):
                        self.vec[i] = tuple(GameState.Camera.world2render(0.01*self.rendersize*v + self.pos))

                    # draw triangle
                    g.draw.polygon(GameState.display, Colors.orange, self.vec)

                    # draw dot at ship position itself
                    g.draw.circle(GameState.display, self.color, self.renderpos, self.rendersize)
