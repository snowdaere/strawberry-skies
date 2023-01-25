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


        self.color = data['color']
        self.name = data['name']
        
    def render(self, display):
        # radius to be drawn on the screen
        rendersize = Camera.camzoom*(self.radius)
        drawcircle(display, world2render(self.pos), rendersize, self.color)

    def updatepos(self, t):
        pass


class Sattelite:
    def __init__(self, parent:Body, distance:float, mass:float, data:dict) -> None:
        self.parent = parent
        self.distance = distance

        # position in the game world
        ### NOTE in the future make this pick a random position along the circle to render
        self.pos = self.parent.pos + np.array((self.distance, 0))
        # mass (for physics)
        self.mass = mass
        # radius of planet
        self.radius = math.atan(self.mass)

        self.omega = (1/distance)*(math.sqrt(GameState.G * (self.mass + self.parent.mass))/math.sqrt(self.distance))

        self.color = data['color']
        self.name = data['name']


    def updatepos(self, t):
        # Calculate new position
        self.pos = self.parent.pos + self.distance*np.array((np.cos(self.omega*t), np.sin(self.omega*t)))



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

class FreeBody:
    def __init__(self, x:float, y:float, color):
        # physics variables
        self.pos = np.array((x, y))
        self.vel = np.array((0.0, 0.0))
        self.acc = np.array((0.0, 0.0))
        self.color = color

        #self.theta = np.arctan(self.vel[1]/self.vel[0])

        # gameplay information
        self.orbiting = None

    def render(self, display):
        # DEFAULT IS 0.01
        rendersize = int(Camera.camzoom*(0.1))

        g.draw.circle(display, self.color, world2render(self.pos), rendersize)

    def getdistfrom(self, object):
        dx = self.pos[0] - object.pos[0]
        dy = self.pos[1] - object.pos[1]
        return np.sqrt(dx**2 + dy**2)

    def getunit(self, object:Union[Body, Sattelite]):
        '''returns unit vector pointing at the object'''
        return (self.pos-object.pos)/self.getdistfrom(object)

    def getaccel(self, bodies):
        acc = np.array((0, 0))
        for body in bodies:
            r = self.getdistfrom(body)
            acc  = acc -1*GameState.G*body.mass*(1/r**2)*self.getunit(body)
        self.acc = acc


    

    def update(self):
        if self.orbiting is None:
            # calculate acceleration
            acc = np.array((0.0, 0.0))
            for body in Bodies:
                r = self.getdistfrom(body)
                acc  = acc - GameState.G*body.mass*(1/r**2)*self.getunit(body)
            self.acc = acc


            # here, if the ship is not orbiting anything
            ### NOTE use verlet integration for this you fool
            self.vel = self.vel + (GameState.dt * self.acc)
            self.pos = self.pos + (GameState.dt * self.vel)
            
        else:
            # here, movement if the ship is orbiting something
            pass




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

def render():
    # handle screen
    if MainScreen:
        
        # draw background
        display.fill(Colors.black)

        # render planets
        for body in Bodies:
            body.render(display)
        
        Player.render(display)

        # render comets
        for comet in comets:
            comet.render(display)

        
        
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

    # handle key presses
    if event.type == g.KEYDOWN:
        if event.key == g.K_ESCAPE:
            print('Escape was pressed')
            # do pausing
            GameState.Paused = not GameState.Paused
            if Paused:
                print('Game Paused')
            if not Paused:
                print('Game Unpaused')
        # implement forced crash
        if event.key == g.K_DELETE:
            print('Quitting')
            running = False
            g.quit()
            quit()
        if event.key == g.K_q:
            # toggle panning mode
            Camera.campos = np.floor(Player.pos)
            Camera.camzoom = Camera.camzoommax

            
def update():

    if not GameState.Paused:
        # update the game time
        GameState.t += GameState.dt


        # update the planet position based on time
        for planet in System1.System:
            planet.updatepos(GameState.t)

        # update ships
        Player.update()


        
        for comet in comets:
            comet.update()
    else:
        pass
        


def main():
    '''do the game stuff'''
    for event in g.event.get():
        handle(event)
    
    update()

    render()
    clock.tick(FPS)
    print(clock.get_fps())



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
    flags = g.HWSURFACE
    display = g.display.set_mode(Camera.dim, flags, vsync=1)
    g.display.set_caption('Strawberry Skies')
    clock = g.time.Clock()
    display.fill(Colors.black)
    #font = g.font.Font('Freesansbold.ttf', 32)
    
    FPS = 60
    running = True

    # set icon
    img = g.image.load('strawberry.png')
    g.display.set_icon(img)


    # Create the world to be rendered
    ## GAME WORLD
    Bodies = System1.System

    Player = FreeBody(33, 5, Colors.purple)
    comets = []
    for i in range(1000):
        comets.append(FreeBody(r.randrange(-40, 40), r.randrange(-40, 40), Colors.red))

    while running:
        main()