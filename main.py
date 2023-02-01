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
import Ship
import Handle

'''it has been 6 billion years. i am the collected consciousness of all humanity, ascended to existence in the electrical and gravitational fields that permeate the galaxy as a single giant neural network. the galaxy is so expanded that the light of one star no longer reaches another. i am still playing strawberry skies'''


def drawcircle(surface, pos, r, color):
    pos = np.int64(pos)
    draw.filled_circle(surface, *pos, int(r), color)
    draw.aacircle(surface, *pos, int(r), color)


class Body:
    def __init__(self, pos: np.ndarray, mass, data) -> None:
        # position in the game world
        self.pos = pos
        self.vel = np.array((0, 0))
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
        drawcircle(display, Camera.world2render(self.pos), rendersize, self.color)

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
        g.draw.circle(display, Colors.white, Camera.world2render(self.parent.pos), Camera.camzoom*self.distance, width=1)
        
        # render the planet itself
        drawcircle(display, Camera.world2render(self.pos), rendersize, self.color)

# import test system
import System1




def say(string, color, xy):
    display.blit(font.render(string, False, color), xy)


def render(Player):
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
        say(f'Zoom: {Camera.campos}', Colors.white, (10, 115))

        
        # draw orbit brackets around selected body
        color = Colors.black
        if not Player.orbiting:
            if Player.selected.minorbit <= Player.selecteddist <= Player.selected.maxorbit:
                color = Colors.yellow
            else:
                color = Colors.red
        else:
            color = Colors.green

        if not Player.dead:
            # if Player.selectionhold:
            # # draw blue marker around nearest planet if selected hold
            #     g.draw.circle(display, Colors.blue, Camera.world2render(Player.nearest.pos), Camera.camzoom*Player.nearest.minorbit, width=1)
            #     g.draw.circle(display, Colors.blue, Camera.world2render(Player.nearest.pos), Camera.camzoom*Player.nearest.maxorbit, width=1)



            # draw orbit brackets around selected planet
            g.draw.circle(display, color, Camera.world2render(Player.selected.pos), Camera.camzoom*Player.selected.minorbit, width=1)
            g.draw.circle(display, color, Camera.world2render(Player.selected.pos), Camera.camzoom*Player.selected.maxorbit, width=1)

            linecolor = Colors.red
            if Player.selectionhold:
                linecolor = Colors.blue
            # draw vector to selected planet
            g.draw.line(display, linecolor, Camera.world2render(Player.pos), Camera.world2render(Player.selected.pos))

            # draw vector pointing from player to mouse pos
            thrustcolor = Colors.purple
            if Player.thrusting:
                thrustcolor = Colors.green
            g.draw.line(display, thrustcolor, Camera.world2render(Player.pos), g.mouse.get_pos())


        
        
        # flip display
        g.display.flip()
        ### NOTE this might break in the future when the game is going on long, because without the drawing of the backgrund/
        ### it doesnt work; the previous frame is still rendered
    
    elif Paused:
        pass

        
def update():
    '''update the game state'''
    if not GameState.Paused:
        # update the game time
        GameState.t += GameState.dt


        # update the planet position based on time
        for planet in System1.System:
            planet.update(GameState.t)

        # update Player
        Player.update()

        # update camera position if following
        if Camera.Follow:
            Camera.campos = Player.pos

    else:
        pass


def main():
    '''do the game stuff'''
    for event in g.event.get():
        Handle.handle(event, Player)
    
    update()

    render(Player)
    clock.tick(GameState.FPS)



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

    # initialize fint
    g.font.init()
    font = g.font.SysFont('Courier', 20)
    
    # set icon
    img = g.image.load('strawberry.png')
    g.display.set_icon(img)


    # Create the world to be rendered
    ## GAME WORLD
    Bodies = System1.System

    Player = Ship.Player(33, 5, Colors.purple)
    
    while GameState.running:
        main()