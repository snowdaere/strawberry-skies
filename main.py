import pygame as g
import math
from dotmap import DotMap
import numpy as np
import random as r


class Body:
    def __init__(self, x, y, mass, color) -> None:
        # position in the game world
        self.pos = self.x, self.y = np.array((x, y))
        # mass (for physics)
        self.mass = mass
        # radius of planet
        self.radius = math.atan(self.mass)


        self.color = color
        
        
        

    def render(self):
        # radius to be drawn on the screen
        rendersize = camzoom*(self.radius)
        g.draw.circle(display, self.color, world2render(self.pos), rendersize)


class Ship:
    def __init__(self, x, y) -> None:
        # physics variables
        self.pos = np.array((x, y))
        self.vel = 0, 0
        self.acc = 0, 0





## GENERAL GAME ESTABLISHMENT
# define game variables
dim = width, height = np.array((800, 800))
# the center vector points from the corner of the screen to the middle
center = np.array((width/2, height/2))





## CAMERA CODE
# initialize the camera settings
# is the scale setting, or how many display pixels make a game unit
camzoomdefault = 100
camzoom = camzoomdefault
campos = camx, camy = np.array((0, 4))

# this object is used to flip the screen coordinates to a standard x/y orientation
flip1 = np.array((1, -1))
flip2 = np.array((-1, 1))

# Says whether the game is panning or not (to update the campos)
Panning = False
# dummy variable used for holding offset while panning
PanStartPos = np.array((0, 0))
CamPosStart = np.array((0, 0))
CamPosOffset = np.array((0, 0))

# Says what screen the game is in
MainScreen = True
Paused = False

# Color Palette
colors = DotMap({
    'black': (13, 1, 6),
    'brown': (97, 80, 85),
    'red': (211, 59, 105),
    'salmon': (232, 236, 115),
    'orange': (255, 180, 139),
    'yellow': (243, 223, 162),
    'green': (77, 204, 189),
    'blue': (87, 142, 255),
    'purple': (126, 111, 255),
})

planetcolors = [colors.red, colors.salmon, colors.orange, colors.yellow, colors.green, colors.blue, colors.purple]

def zoomout():
    global camzoom
    if camzoom > 0.0625*camzoomdefault:
        camzoom *= 0.5

def zoomin():
    global camzoom
    if camzoom < 4*camzoomdefault:
        camzoom *= 2

def mouse():
    return np.array(g.mouse.get_pos())

def render2world(renderpos:np.array):
    '''Transforms camera coordinates to in-world coordinates'''
    return flip1*((1/camzoom)*(renderpos - center) - flip2*campos)

def world2render(worldpos:np.array):
    '''Transforms in-world coordinates to camera coordinates'''
    return center + camzoom*(flip2*campos + flip1*worldpos)

def render():
    if MainScreen:
        global Panning, campos
        # Handle Game States


        # draw background
        display.fill(colors.black)

        for body in bodies:
            body.render()

        # flip display
        g.display.flip()
        ### NOTE this might break in the future when the game is going on long, because without the drawing of the backgrund/
        ### it doesnt work; the previous frame is still rendered
    
    elif Paused:
        pass

    

## GAME WORLD
bodies = [Body(0, 0, 1, colors.red), Body(2, 2, 2, colors.blue), Body(0, 4, 0.5, colors.green)]
# make lots of planets
for i in range(100):
    bodies.append(Body(r.randrange(-40, 40), r.randrange(-40, 40), r.randrange(1, 3), r.choice(planetcolors)))



## GAME FUNCTIONS
def handle(event:g.event):
    global Panning, Paused, PanStartPos, CamPosStart, running, campos, CamPosOffset
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
            Panning = True
            CamPosStart = campos
            CamPosOffset = campos - render2world(mouse())

    if event.type == g.MOUSEBUTTONUP:
        if event.button == 1:
            print('you left unclicked')
        if event.button == 3:
            # implement panning with the right mouse button
            # set camera position to the current mouse location
            print('you right unclicked')
            Panning = False

    if event.type == g.MOUSEMOTION:
        if Panning:
            campos = CamPosStart - (-campos + render2world(mouse())) - CamPosOffset

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

            
            
        


def main():
    '''do the game stuff'''
    for event in g.event.get():
        handle(event)

    render()
    clock.tick(FPS)


if __name__ == '__main__':
    # initialize the game stuff
    display = g.display.set_mode(dim)
    g.display.set_caption('Strawberry Skies')
    clock = g.time.Clock()
    display.fill(colors.black)
    
    FPS = 60
    running = True


    while running:
        main()