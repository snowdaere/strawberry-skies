# import libraries
import pygame as g
import time
import random as r

# import Game Modules
from GameState import GameState
import Rendering.Colors as Colors
import Rendering.Render as Render
import Rendering.HUD as HUD
import Entities.Player as Player
import Entities.Freebody as Freebody
import Handle
# import camera to load into game
from Rendering.Camera import Camera

'''it has been 6 billion years. i am the collected consciousness of all humanity, 
ascended to existence in the electrical and gravitational fields that permeate 
the galaxy as a single giant neural network. the galaxy is so expanded that 
 the light of one star no longer reaches another. 
 i am still playing strawberry skies'''

  
def update():
    '''update the game state'''
    if not GameState.Paused:
        # update the game time
        GameState.t += GameState.dt

        # update the planet position based on time
        for body in GameState.Bodies:
            body.update()


        for entity in GameState.Entities:
            entity.update()

        # update Player
        GameState.Player.update()

    else:
        pass



if __name__ == '__main__':
    # set the camera
    GameState.Camera = Camera
    # Create the world
    ## GAME WORLD
    import System1
    GameState.Bodies = System1.System
    GameState.Player = Player.Player(33, 5, Colors.purple)
    # spawn a bunch of physics objects?
    # GameState.Entities = [Freebody.Freebody(r.randrange(-40, 40), r.randrange(-40, 40), Colors.red) for i in range(250)]

    # timing stuff
    previous = time.time()
    lag = 0.0
    # calculate ticks per second
    tickstart = time.time()
    tickend = 0.0
    tickelapsed = 1.0
    ticklength = 0.0
    
    update()

    while GameState.running:
        current = time.time()

        elapsed = current - previous
        previous = current
        lag += elapsed

        '''handle input, update, render'''
        for event in g.event.get():
            Handle.handle(event)
        
        while lag >= GameState.dt:
            pretick = time.time()
            update()
            # frame system
            lag -= GameState.dt
            # tick system
            tickend = time.time()
            tickelapsed = tickend - tickstart
            tickstart = time.time()
            ticklength = tickend - pretick


        Render.render()
        HUD.say(f'FPS: {1/elapsed:5.2f}', Colors.white, (10, 10))
        HUD.say(f'TPS: {1/tickelapsed:5.2f} / MSPT: {1000*ticklength:5.3f}', Colors.white, (10, 25))

        # flip display
        g.display.flip()
        # render ms per frame
