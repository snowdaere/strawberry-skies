import numpy as np
import pygame as g
import pygame.gfxdraw as draw

from GameState import GameState
import Rendering.Colors as Colors
import Rendering.HUD as HUD


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

        HUD.renderHUD()

        