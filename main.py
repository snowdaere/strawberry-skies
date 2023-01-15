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
        g.draw.circle(display, self.color, center + camzoom*(flip2*campos + flip1*self.pos), rendersize)


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

def pan(dpos:np.array):
    campos = np.multiply(np.add(campos, dpos), camzoom)

def render2world(renderpos:np.array):
    '''Transforms camera coordinates to in-world coordinates'''
    return flip1*((1/camzoom)*(renderpos - center) - flip2*campos)

def world2render(worldpos:np.array):
    '''Transforms in-world coordinates to camera coordinates'''
    return center + camzoom*(flip2*campos + flip1*worldpos)

def render():
    # draw background
    display.fill(colors.black)
    
    for body in bodies:
        body.render()
    
    # flip display
    g.display.flip()
    ### NOTE this might break in the future when the game is going on long, because without the drawing of the backgrund/
    ### it doesnt work; the previous frame is still rendered

    

## GAME WORLD
bodies = [Body(0, 0, 1, colors.red), Body(2, 2, 2, colors.blue), Body(0, 4, 0.5, colors.green)]
# make lots of planets
for i in range(100):
    bodies.append(Body(r.randrange(-40, 40), r.randrange(-40, 40), r.randrange(1, 3), r.choice(planetcolors)))



## GAME FUNCTIONS
def handle(event:g.event):
    global campos
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
            print('you right clicked!')
            campos = render2world(np.array(g.mouse.get_pos()))
            print(campos)
            
        


def main():
    '''do the game stuff'''
    for event in g.event.get():
        handle(event)

    render()
    clock.tick(60)


if __name__ == '__main__':
    # initialize the game stuff
    display = g.display.set_mode(dim)
    g.display.set_caption('Strawberry Skies')
    clock = g.time.Clock()
    display.fill(colors.black)

    running = True


    while running:
        main()