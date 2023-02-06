import numpy as np
import pygame as g
import pygame.gfxdraw as draw

from GameState import GameState
import Rendering.Colors as Colors


def say(display, string, color, xy):
    '''spits a changing string onto a position on screen'''
    display.blit(GameState.font.render(string, False, color), xy)

def drawcircle(surface, pos, r, color):
    '''draws anti-aliased circle at position'''
    pos = np.int64(pos)
    draw.filled_circle(surface, *pos, int(r), color)
    draw.aacircle(surface, *pos, int(r), color)

def render():
    '''general render command for the game'''
    # handle screen
    if GameState.MainScreen:
        # update camera position if following
        if GameState.Camera.Follow:
            GameState.Camera.campos = GameState.Player.pos
        
        # draw background
        GameState.display.fill(Colors.black)

        # render planets
        for body in GameState.Bodies:
            body.render()
        # render entities
        for entity in GameState.Entities:
            entity.render()
        


        ## render player and HUD information
        GameState.Player.render()

        ## render orbit HUD
        # render text info
        say(GameState.display, f'Time: {GameState.t:.2f}', Colors.white, (10, 40))
        say(GameState.display, f'Paused: {GameState.Paused}', Colors.white, (10, 55))
        say(GameState.display, f'Nearest: {GameState.Player.nearest.name}', GameState.Player.nearest.color, (10, 70))
        if GameState.Player.selectionhold:
            say(GameState.display, f'Selected: {GameState.Player.selected.name}', GameState.Player.selected.color, (10, 85))
        if GameState.Player.orbiting:
            say(GameState.display, f'Orbiting: {GameState.Player.orbit.name}', GameState.Player.orbit.color, (10, 100))
        if GameState.Player.dead:
            say(GameState.display, f'You Died', Colors.red, (10, 115))
        say(GameState.display, f'Max Orbit: {GameState.Player.selected.maxorbit}', Colors.white, (10, 130))
        say(GameState.display, f'dsitance: {GameState.Player.selecteddist}', Colors.white, (10, 145))


        
        # draw orbit brackets around selected body
        color = Colors.black
        if not GameState.Player.orbiting:
            if GameState.Player.selected.minorbit <= GameState.Player.selecteddist <= GameState.Player.selected.maxorbit:
                color = Colors.yellow
            else:
                color = Colors.red
        else:
            color = Colors.green

        if not GameState.Player.dead:
            # if Player.selectionhold:
            # # draw blue marker around nearest planet if selected hold
            #     g.draw.circle(display, Colors.blue, Camera.world2render(Player.nearest.pos), Camera.camzoom*Player.nearest.minorbit, width=1)
            #     g.draw.circle(display, Colors.blue, Camera.world2render(Player.nearest.pos), Camera.camzoom*Player.nearest.maxorbit, width=1)



            # draw orbit brackets around selected planet
            g.draw.circle(GameState.display, color, GameState.Camera.world2render(GameState.Player.selected.pos), GameState.Camera.camzoom*GameState.Player.selected.minorbit, width=1)
            g.draw.circle(GameState.display, color, GameState.Camera.world2render(GameState.Player.selected.pos), GameState.Camera.camzoom*GameState.Player.selected.maxorbit, width=1)

            linecolor = Colors.red
            if GameState.Player.selectionhold:
                linecolor = Colors.blue
            # draw vector to selected planet
            g.draw.line(GameState.display, linecolor, GameState.Camera.world2render(GameState.Player.pos), GameState.Camera.world2render(GameState.Player.selected.pos))

            # draw vector pointing from player to mouse pos
            thrustcolor = Colors.purple
            if GameState.Player.thrusting:
                thrustcolor = Colors.green
            g.draw.line(GameState.display, thrustcolor, GameState.Camera.world2render(GameState.Player.pos), g.mouse.get_pos())


        
        

        ### NOTE this might break in the future when the game is going on long, because without the drawing of the backgrund/
        ### it doesnt work; the previous frame is still rendered
    
    elif GameState.Paused:
        pass