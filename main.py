# import libraries
import pygame as g
import math
import numpy as np
import random as r

# import Game Modules
import GameState
import Rendering.Camera as Camera
import Rendering.Colors as Colors
import Rendering.Render as Render
import Entities.Player as Player
import Entities.Body as Body
import Entities.Sattelite as Sattelite
import Handle

'''it has been 6 billion years. i am the collected consciousness of all humanity, 
ascended to existence in the electrical and gravitational fields that permeate 
the galaxy as a single giant neural network. the galaxy is so expanded that 
 the light of one star no longer reaches another. 
 i am still playing strawberry skies'''

# import test system
import System1
  
def update():
    '''update the game state'''
    if not GameState.Paused:
        # update the game time
        GameState.t += GameState.dt


        # update the planet position based on time
        for planet in System1.System:
            planet.update(GameState.t)

        # update Player
        Player0.update(GameState.Bodies)

        # update camera position if following
        if Camera.Follow:
            Camera.campos = Player0.pos

    else:
        pass


def main():
    '''handle, update, render'''
    for event in g.event.get():
        Handle.handle(event, Player0)
    
    update()

    Render.render(GameState.display, GameState.Bodies, Player0)

    GameState.clock.tick(GameState.FPS)


if __name__ == '__main__':
    
    # Create the world
    ## GAME WORLD
    GameState.Bodies = System1.System

    Player0 = Player.Player(33, 5, Colors.purple)
    
    while GameState.running:
        main()