import numpy as np
import pygame as g
import pygame.gfxdraw as draw

import GameState
import Rendering.Camera as Camera
import Rendering.Colors as Colors
import Entities.Player as Player


def say(display, string, color, xy):
    '''spits a changing string onto a position on screen'''
    display.blit(GameState.font.render(string, False, color), xy)

def drawcircle(surface, pos, r, color):
    '''draws anti-aliased circle at position'''
    pos = np.int64(pos)
    draw.filled_circle(surface, *pos, int(r), color)
    draw.aacircle(surface, *pos, int(r), color)

def render(display, Bodies, Player: Player.Player):
    '''general render command for the game'''
    # handle screen
    if GameState.MainScreen:
        
        # draw background
        display.fill(Colors.black)

        # render planets
        for body in Bodies:
            body.render(display)
        


        ## render player and HUD information
        Player.render(display)

        ## render orbit HUD
        # render text info
        say(display, f'FPS: {GameState.clock.get_fps():.1f}', Colors.white, (10, 10))
        say(display, f'Time: {GameState.t:.2f}', Colors.white, (10, 25))
        say(display, f'Paused: {GameState.Paused}', Colors.white, (10, 40))
        say(display, f'Nearest: {Player.nearest.name}', Player.nearest.color, (10, 55))
        if Player.selectionhold:
            say(display, f'Selected: {Player.selected.name}', Player.selected.color, (10, 70))
        if Player.orbiting:
            say(display, f'Orbiting: {Player.orbit.name}', Player.orbit.color, (10, 85))
        if Player.dead:
            say(display, f'You Died', Colors.red, (10, 100))
        say(display, f'Max Orbit: {Player.selected.maxorbit}', Colors.white, (10, 115))
        say(display, f'dsitance: {Player.selecteddist}', Colors.white, (10, 130))


        
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
    
    elif GameState.Paused:
        pass