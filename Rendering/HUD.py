import pygame as g
import numpy as np

from GameState import GameState
import Rendering.Colors as Colors
from Entities.Entity import Entity


def say(string, color, xy):
    '''spits a changeable string onto a position on screen'''
    GameState.display.blit(GameState.font.render(string, False, color), xy)

def renderHUD():
    '''render orbit HUD'''
    # render text info
    say(f'Time: {GameState.t:.2f}', Colors.white, (10, 40))
    say(f'Paused: {GameState.Paused}', Colors.white, (10, 55))
    say(f'Nearest: {GameState.Player.nearest.name}', GameState.Player.nearest.color, (10, 70))
    if GameState.Player.selectionhold:
        say(f'Selected: {GameState.Player.selected.name}', GameState.Player.selected.color, (10, 85))
    if GameState.Player.orbiting:
        say(f'Orbiting: {GameState.Player.orbit.name}', GameState.Player.orbit.color, (10, 100))
    if GameState.Player.dead:
        say(f'You Died', Colors.red, (10, 115))
    say(f'Max Orbit: {GameState.Player.selected.maxorbit}', Colors.white, (10, 130))
    say(f'dsitance: {GameState.Player.selecteddist}', Colors.white, (10, 145))


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

    # if paused, render planet names and pause screen
    if GameState.Paused:
        for body in GameState.Bodies:
            body.label()
            
    
    

    ### NOTE this might break in the future when the game is going on long, because without the drawing of the backgrund/
    ### it doesnt work; the previous frame is still rendered
