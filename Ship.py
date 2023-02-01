import numpy as np
import Camera
import GameState
import Colors
import pygame as g
import System1

Bodies = System1.System

class Ship:
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

    def render(self, display):
        # DEFAULT IS 0.01
        rendersize = int(Camera.camzoom*(0.01))

        # draw orbit brackets around selected body
        color = Colors.black
        if not self.orbiting:
            if self.selected.minorbit <= self.selecteddist <= self.selected.maxorbit:
                color = Colors.yellow
            else:
                color = Colors.red
        else:
            color = Colors.green

        if not self.dead:
            # if self.selectionhold:
            # # draw blue marker around nearest planet if selected hold
            #     g.draw.circle(display, Colors.blue, Camera.world2render(self.nearest.pos), Camera.camzoom*self.nearest.minorbit, width=1)
            #     g.draw.circle(display, Colors.blue, Camera.world2render(self.nearest.pos), Camera.camzoom*self.nearest.maxorbit, width=1)



            # draw orbit brackets around selected planet
            g.draw.circle(display, color, Camera.world2render(self.selected.pos), Camera.camzoom*self.selected.minorbit, width=1)
            g.draw.circle(display, color, Camera.world2render(self.selected.pos), Camera.camzoom*self.selected.maxorbit, width=1)

            linecolor = Colors.red
            if self.selectionhold:
                linecolor = Colors.blue
            # draw vector to selected planet
            g.draw.line(display, linecolor, Camera.world2render(self.pos), Camera.world2render(self.selected.pos))

            # draw vector pointing from player to mouse pos
            thrustcolor = Colors.purple
            if self.thrusting:
                thrustcolor = Colors.green
            g.draw.line(display, thrustcolor, Camera.world2render(self.pos), g.mouse.get_pos())

        # draw ship itself
        g.draw.circle(display, self.color, Camera.world2render(self.pos), rendersize)

        


    def getdistfrom(self, object):
        dx = self.pos[0] - object.pos[0]
        dy = self.pos[1] - object.pos[1]
        return np.sqrt(dx**2 + dy**2)

    def updatedist(self, bodies):
        for i, object in enumerate(bodies):
            self.distances[i] = self.getdistfrom(object)

    def getunit(self, object):
        '''returns unit vector pointing at the object'''
        return (self.pos-object.pos)/self.getdistfrom(object)

    def thrust(self):
        mousepos = Camera.render2world(g.mouse.get_pos())
        dif = self.pos-mousepos
        unit = (dif)/np.sqrt(dif[0]**2 + dif[1]**2)
        self.thrusting = True
        return unit*(self.thrustforce/self.mass)

    def updateaccel(self, bodies):
        acc = np.array((0, 0))
        for i, r in enumerate(self.distances):
            body = bodies[i]
            acc  = acc -1*GameState.G*body.mass*(1/r**2)*self.getunit(body)
        if self.thrusting:
            acc -= self.thrust()
        self.acc = acc

    def setnearest(self, bodies):
        min = 1000
        mindex = -1
        for i, dist in enumerate(self.distances):
            if dist < min:
                min = dist
                mindex = i
        self.nearest = bodies[mindex]
        self.nearestdist = min
        self.nearestinit = self.pos - self.nearest.pos

        # do selection logic, depengin
        if self.selectionhold:        
            self.selecteddist = self.nearestdist
        if not self.selectionhold:
            self.selected = self.nearest

    def attemptorbit(self):
        # attempt to orbit the nearest body if within bracket
        ### TODO make it so that you must approach within 45 degrees of the orbital face to engage orbit
        ### and change the orbit bracket colors to match 
        
        if self.selected.minorbit <= self.selecteddist <= self.selected.maxorbit:
            self.orbiting = True
            self.orbit = self.selected
            self.orbitinit = self.nearestinit
    
    def deorbit(self):
        self.orbiting = False

    def respawn(self):
        if self.dead:
            self.dead = False
            # place you in orbital bracket behind planet
            self.pos = self.nearest.pos + 2*self.nearest.radius
            self.vel = self.nearest.vel






    

    def update(self):
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