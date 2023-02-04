# import libraries
import pygame as g
import time

# import Game Modules
import GameState
import Rendering.Camera as Camera
import Rendering.Colors as Colors
import Rendering.Render as Render
import Entities.Player as Player
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



if __name__ == '__main__':
    # Create the world
    ## GAME WORLD
    GameState.Bodies = System1.System

    Player0 = Player.Player(33, 5, Colors.purple)

    # timing stuff
    previous = time.time()
    lag = 0.0
    update()

    while GameState.running:
        current = time.time()
        elapsed = current - previous
        previous = current
        lag += elapsed

        '''handle input, update, render'''
        for event in g.event.get():
            Handle.handle(event, Player0)
        
        while lag >= GameState.dt:
            update()
            lag -= GameState.dt

        Render.render(GameState.display, GameState.Bodies, Player0)
        Render.say(GameState.display, f'FPS: {1/elapsed:.2f}', Colors.white, (10, 10))

        # flip display
        g.display.flip()
        # render ms per frame
