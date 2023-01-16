# import libraries
import pygame as g
import math
import numpy as np
import random as r

# import modules
import Camera
import Colors


class Body:
    def __init__(self, pos: np.ndarray, velocity: np.ndarray, mass, color) -> None:
        # position in the game world
        self.pos = pos
        # mass (for physics)
        self.mass = mass
        # radius of planet
        self.radius = math.atan(self.mass)


        self.color = color
        
    def render(self):
        # radius to be drawn on the screen
        rendersize = Camera.camzoom*(self.radius)
        g.draw.circle(display, self.color, world2render(self.pos), rendersize)

class Star(Body):
    pass

class Planet(Body):
    pass        

class Ship:
    def __init__(self, x, y) -> None:
        # physics variables
        self.pos = np.array((x, y))
        self.vel = 0, 0
        self.acc = 0, 0


def zoomout():
    if Camera.camzoom > 0.0625*Camera.camzoomdefault:
        Camera.camzoom *= 0.5

def zoomin():
    if Camera.camzoom < 4*Camera.camzoomdefault:
        Camera.camzoom *= 2

def mouse():
    return np.array(g.mouse.get_pos())

def render2world(renderpos:np.array):
    '''Transforms camera coordinates to in-world coordinates'''
    return Camera.flip1*((1/Camera.camzoom)*(renderpos - center) - Camera.flip2*Camera.campos)

def world2render(worldpos:np.array):
    '''Transforms in-world coordinates to camera coordinates'''
    return center + Camera.camzoom*(Camera.flip2*Camera.campos + Camera.flip1*worldpos)

def render():
    if MainScreen:
        # Handle Game States


        # draw background
        display.fill(Colors.black)

        for body in bodies:
            body.render()

        # flip display
        g.display.flip()
        ### NOTE this might break in the future when the game is going on long, because without the drawing of the backgrund/
        ### it doesnt work; the previous frame is still rendered
    
    elif Paused:
        pass


## GAME FUNCTIONS
def handle(event:g.event):
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
            Camera.Panning = True
            Camera.CamPosStart = Camera.campos
            Camera.CamPosOffset = Camera.campos - render2world(mouse())

    if event.type == g.MOUSEBUTTONUP:
        if event.button == 1:
            print('you left unclicked')
        if event.button == 3:
            # implement panning with the right mouse button
            # set camera position to the current mouse location
            print('you right unclicked')
            Camera.Panning = False

    if event.type == g.MOUSEMOTION:
        if Camera.Panning:
            Camera.campos = Camera.CamPosStart - (-Camera.campos + render2world(mouse())) - Camera.CamPosOffset

    # handle key presses
    if event.type == g.KEYDOWN:
        if event.key == g.K_ESCAPE:
            print('Escape was pressed')
            # do pausing
            Paused = not Paused
            if Paused:
                print('Game Paused')
            if not Paused:
                print('Game Unpaused')

            
def update():
    if not GameState.Paused:
        # update the game system
        pass
    else:
        pass
        


def main():
    '''do the game stuff'''
    for event in g.event.get():
        handle(event)
    
    update()

    render()
    clock.tick(FPS)


class GameState:
    # Says what screen the game is in
    MainScreen = True
    Paused = False

    FPS = 60
    running = True
    dt = 1/FPS

    # Define universal constants
    # gravitational constant
    G = 1






if __name__ == '__main__':
    # initialize basic stuff
    ## GENERAL GAME ESTABLISHMENT
    # define game variables
    dim = width, height = np.array((800, 800))
    # the center vector points from the corner of the screen to the middle
    center = np.array((width/2, height/2))


    # Says what screen the game is in
    MainScreen = True
    Paused = False

    
    # initialize the game stuff
    display = g.display.set_mode(dim)
    g.display.set_caption('Strawberry Skies')
    clock = g.time.Clock()
    display.fill(Colors.black)
    
    FPS = 60
    running = True


    # Create the world to be rendered
    ## GAME WORLD
    bodies = [Body(np.array((0, 0)), 1, 1, Colors.red), Body(np.array((2, 2)), 2, 2, Colors.blue), Body(np.array((0, 4)), 4, 0.5, Colors.green)]
    # make lots of planets
    #for i in range(100):
    #    bodies.append(Body(np.array(r.randrange(-40, 40), r.randrange(-40, 40)), r.randrange(1, 3), r.choice(planetcolors)))


    while running:
        main()