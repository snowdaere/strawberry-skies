# import libraries
import pygame as g
from pygame import gfxdraw as draw
import math
import numpy as np
import random as r
from typing import Union

# import modules
import Camera
import Colors
import GameState

'''it has been 6 billion years. i am the collected consciousness of all humanity, ascended to existence in the electrical and gravitational fields that permeate the galaxy as a single giant neural network. the galaxy is so expanded that the light of one star no longer reaches another. i am still playing strawberry skies'''


def drawcircle(surface, pos, r, color):
    pos = np.int64(pos)
    draw.filled_circle(surface, *pos, int(r), color)
    draw.aacircle(surface, *pos, int(r), color)


class Body:
    def __init__(self, pos: np.ndarray, mass, data) -> None:
        # position in the game world
        self.pos = pos
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
        drawcircle(display, world2render(self.pos), rendersize, self.color)

    def update(self, t):
        pass


class Sattelite:
    def __init__(self, parent:Body, distance:float, mass:float, data:dict) -> None:
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
        # Calculate new position
        self.pos = self.parent.pos + self.distance*np.array((np.cos(self.omega*t), np.sin(self.omega*t)))
        self.vel = self.distance*self.omega*np.array((-1*np.sin(self.omega*t), np.cos(self.omega*t)))


    def render(self, display):
        # radius to be drawn on the screen
        rendersize = int(Camera.camzoom*(self.radius))

        # render the orbit
        #draw.aacircle(display, *np.int64(world2render(self.parent.pos)), int(Camera.camzoom*self.distance), Colors.white)
        g.draw.circle(display, Colors.white, world2render(self.parent.pos), Camera.camzoom*self.distance, width=1)
        
        # render the planet itself
        drawcircle(display, world2render(self.pos), rendersize, self.color)

# import test system
import System1

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

    def render(self, display):
        # DEFAULT IS 0.01
        rendersize = int(Camera.camzoom*(0.01))

        # draw orbit brackets around nearest body
        color = Colors.black
        if not self.orbiting:
            if self.selected.minorbit <= self.selecteddist <= self.selected.maxorbit:
                color = Colors.yellow
            else:
                color = Colors.red
        else:
            color = Colors.green

        if not self.dead:
            # draw orbit brackets around selected planet
            g.draw.circle(display, color, world2render(self.selected.pos), Camera.camzoom*self.selected.minorbit, width=1)
            g.draw.circle(display, color, world2render(self.selected.pos), Camera.camzoom*self.selected.maxorbit, width=1)


            # draw vector to selected planet
            g.draw.line(display, Colors.red, world2render(self.pos), world2render(self.selected.pos))

        # draw ship itself
        g.draw.circle(display, self.color, world2render(self.pos), rendersize)

        


    def getdistfrom(self, object):
        dx = self.pos[0] - object.pos[0]
        dy = self.pos[1] - object.pos[1]
        return np.sqrt(dx**2 + dy**2)

    def updatedist(self, bodies):
        for i, object in enumerate(bodies):
            self.distances[i] = self.getdistfrom(object)

    def getunit(self, object:Union[Body, Sattelite]):
        '''returns unit vector pointing at the object'''
        return (self.pos-object.pos)/self.getdistfrom(object)

    def updateaccel(self, bodies):
        acc = np.array((0, 0))
        for i, r in enumerate(self.distances):
            body = bodies[i]
            acc  = acc -1*GameState.G*body.mass*(1/r**2)*self.getunit(body)
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

        # automatically deselect
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




def zoomout():
    if Camera.camzoom > Camera.camzoommin:
        Camera.camzoom *= 0.5

def zoomin():
    if Camera.camzoom < Camera.camzoommax:
        Camera.camzoom *= 2

def mouse():
    return np.array(g.mouse.get_pos())

def render2world(renderpos:np.array):
    '''Transforms camera coordinates to in-world coordinates'''
    return Camera.flip1*((1/Camera.camzoom)*(renderpos - Camera.center) - Camera.flip2*Camera.campos)

def world2render(worldpos:np.array):
    '''Transforms in-world coordinates to camera coordinates'''
    return Camera.center + Camera.camzoom*(Camera.flip2*Camera.campos + Camera.flip1*worldpos)

def say(string, color, xy):
    display.blit(font.render(string, False, color), xy)


def render():
    # handle screen
    if MainScreen:
        
        # draw background
        display.fill(Colors.black)

        # render planets
        for body in Bodies:
            body.render(display)
        


        ## render player and HUD information
        Player.render(display)

        # render orbit HUD


        # render text info
        say(f'FPS: {clock.get_fps():.1f}', Colors.white, (10, 10))
        say(f'Time: {GameState.t:.2f}', Colors.white, (10, 25))
        say(f'Paused: {GameState.Paused}', Colors.white, (10, 40))
        say(f'Nearest: {Player.nearest.name}', Player.nearest.color, (10, 55))
        if Player.selectionhold:
            say(f'Selected: {Player.selected.name}', Player.selected.color, (10, 70))
        if Player.orbiting:
            say(f'Orbiting: {Player.orbit.name}', Player.orbit.color, (10, 85))
        if Player.dead:
            say(f'You Died', Colors.red, (10, 100))


        
        
        # flip display
        g.display.flip()
        ### NOTE this might break in the future when the game is going on long, because without the drawing of the backgrund/
        ### it doesnt work; the previous frame is still rendered
    
    elif Paused:
        pass


## GAME FUNCTIONS
def handle(event:g.event):
    global running
    '''Handle events and stuff'''
    
    if event.type == g.QUIT:

        running = False
        g.quit()
        quit()
    
    # implement zooming
    if event.type == g.MOUSEWHEEL:
        if event.y < 0:
            zoomout()
        if event.y > 0:
            zoomin()
    
    if event.type == g.MOUSEBUTTONDOWN:
        if event.button == 1:
            print('you left clicked')
        if event.button == 3:
            # implement panning with the right mouse button
            # set camera position to the current mouse location
            print('you right clicked')
            Camera.Dragging = True
            Camera.CamPosStart = Camera.campos
            Camera.CamPosOffset = Camera.campos - render2world(mouse())

    if event.type == g.MOUSEBUTTONUP:
        if event.button == 1:
            print('you left unclicked')
        if event.button == 3:
            # implement panning with the right mouse button
            # set camera position to the current mouse location
            print('you right unclicked')
            Camera.Dragging = False

    if event.type == g.MOUSEMOTION:
        if Camera.Dragging:
            Camera.campos = Camera.CamPosStart - (-Camera.campos + render2world(mouse())) - Camera.CamPosOffset
            # if dragging, turn off follow
            Camera.Follow = False

    # handle key presses
    if event.type == g.KEYDOWN:
        if event.key == g.K_ESCAPE:
            # do pausing
            GameState.Paused = not GameState.Paused
        # implement forced crash
        if event.key == g.K_DELETE:
            print('Quitting')
            running = False
            g.quit()
            quit()
        if event.key == g.K_q:
            # toggle following mode
            Camera.Follow = True
        
        if event.key == g.K_r:
            # begin orbiting the planet
            Player.attemptorbit()

        if event.key == g.K_f:
            # get out of the orbit
            Player.deorbit()
        
        if event.key == g.K_w:
            # if orbiting, deorbit
            Player.deorbit()
            # either way, apply thrust
        
        if event.key == g.K_v:
            # lock and unlock selection on a planet
            Player.selectionhold = not Player.selectionhold


            
def update():

    if not GameState.Paused:
        # update the game time
        GameState.t += GameState.dt


        # update the planet position based on time
        for planet in System1.System:
            planet.update(GameState.t)

        # update ships
        Player.update()



        # update camera position if following
        if Camera.Follow:
            Camera.campos = Player.pos



        

    else:
        pass
        


def main():
    '''do the game stuff'''
    for event in g.event.get():
        handle(event)
    
    update()

    render()
    clock.tick(FPS)



if __name__ == '__main__':
    # initialize basic stuff
    ## GENERAL GAME ESTABLISHMENT
    # define game variables
    #Camera.dim = width, height = np.array((800, 800))
    # the center vector points from the corner of the screen to the middle
    #Camera.center = np.array((width/2, height/2))


    # Says what screen the game is in
    MainScreen = True
    Paused = False

    
    # initialize the game stuff
    flags = g.HWSURFACE | g.FULLSCREEN
    display = g.display.set_mode(Camera.dim, flags, vsync=1)
    g.display.set_caption('Strawberry Skies')
    clock = g.time.Clock()
    display.fill(Colors.black)

    g.font.init()
    font = g.font.SysFont('Courier', 20)
    
    FPS = 60
    running = True

    # set icon
    img = g.image.load('strawberry.png')
    g.display.set_icon(img)


    # Create the world to be rendered
    ## GAME WORLD
    Bodies = System1.System

    Player = Ship(33, 5, Colors.purple)
    
    while running:
        main()