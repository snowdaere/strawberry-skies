import numpy as np
import Camera
import GameState
import pygame as g

def handle(event:g.event, Player):
    '''Handle events and stuff'''
    
    if event.type == g.QUIT:
        GameState.running = False
        g.quit()
        quit()
    
    # implement zooming
    if event.type == g.MOUSEWHEEL:
        if event.y < 0:
            Camera.zoomout()
        if event.y > 0:
            Camera.zoomin()
    
    if event.type == g.MOUSEBUTTONDOWN:
        if event.button == 1:
            print('you left clicked')
        if event.button == 3:
            # implement panning with the right mouse button
            # set camera position to the current mouse location
            print('you right clicked')
            Camera.Dragging = True
            Camera.CamPosStart = Camera.campos
            Camera.CamPosOffset = Camera.campos - Camera.render2world(Camera.mouse())

    if event.type == g.MOUSEBUTTONUP:
        if event.button == 1:
            print('you left unclicked')
        if event.button == 3:
            # implement panning with the right mouse button
            # set camera position to the current mouse location
            print('you right unclicked')
            Camera.Dragging = False

    if event.type == g.MOUSEMOTION:
        if Camera.Dragging:
            Camera.campos = Camera.CamPosStart - (-Camera.campos + Camera.render2world(Camera.mouse())) - Camera.CamPosOffset
            # if dragging, turn off follow
            Camera.Follow = False

    # handle key presses
    if event.type == g.KEYDOWN:
        if event.key == g.K_ESCAPE:
            # do pausing
            GameState.Paused = not GameState.Paused
        
        # implement forced crash
        ### NOTE implement actual quit mechanism, remove this after that
        if event.key == g.K_DELETE:
            print('Quitting')
            GameState.running = False
            g.quit()
            quit()
        
        if event.key == g.K_q:
            # toggle following mode
            Camera.Follow = True
        
        if event.key == g.K_r:
            # begin orbiting the planet
            Player.attemptorbit()

        if event.key == g.K_f:
            # get out of the orbit
            Player.deorbit()
        
        if event.key == g.K_w:
            # either way, toggle thrust
            Player.thrusting = True
        
        if event.key == g.K_v:
            # lock and unlock selection on a planet
            Player.selectionhold = not Player.selectionhold
        
        if event.key == g.K_INSERT:
            # respawn key
            Player.respawn()

        # rotation doing
        if event.key == g.K_a:
            Player.rotateCCW = True
        
        if event.key == g.K_a:
            Player.rotateCW = True

    if event.type == g.KEYUP:
        if event.key == g.K_w:
            Player.thrusting = False

        if event.key == g.K_a:
            Player.rotateCCW = False
        
        if event.key == g.K_a:
            Player.rotateCW = False