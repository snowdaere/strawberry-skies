from GameState import GameState
import pygame as g

def handle(event:g.event):
    '''Handle player input and stuff'''
    
    if event.type == g.QUIT:
        GameState.running = False
        g.quit()
        quit()
    
    # implement zooming
    if event.type == g.MOUSEWHEEL:
        if event.y < 0:
            GameState.Camera.zoomout()
        if event.y > 0:
            GameState.Camera.zoomin()
    
    if event.type == g.MOUSEBUTTONDOWN:
        if event.button == 1:
            print('you left clicked')
        if event.button == 3:
            # implement panning with the right mouse button
            # set camera position to the current mouse location
            print('you right clicked')
            GameState.Camera.Dragging = True
            GameState.Camera.CamPosStart = GameState.Camera.campos
            GameState.Camera.CamPosOffset = GameState.Camera.campos - GameState.Camera.render2world(GameState.Camera.mouse())

    if event.type == g.MOUSEBUTTONUP:
        if event.button == 1:
            print('you left unclicked')
        if event.button == 3:
            # implement panning with the right mouse button
            # set camera position to the current mouse location
            print('you right unclicked')
            GameState.Camera.Dragging = False

    if event.type == g.MOUSEMOTION:
        if GameState.Camera.Dragging:
            GameState.Camera.campos = GameState.Camera.CamPosStart - (-GameState.Camera.campos + GameState.Camera.render2world(GameState.Camera.mouse())) - GameState.Camera.CamPosOffset
            # if dragging, turn off follow
            GameState.Camera.Follow = False

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
            GameState.Camera.Follow = True
        
        if event.key == g.K_r:
            # begin orbiting the planet
            GameState.Player.attemptorbit()

        if event.key == g.K_f:
            # get out of the orbit
            GameState.Player.deorbit()
        
        if event.key == g.K_w:
            # either way, toggle thrust
            GameState.Player.thrusting = True
        
        if event.key == g.K_v:
            # lock and unlock selection on a planet
            GameState.Player.selectionhold = not GameState.Player.selectionhold
        
        if event.key == g.K_INSERT:
            # respawn key
            GameState.Player.respawn()

        # rotation doing
        if event.key == g.K_a:
            GameState.Player.rotateCCW = True
        
        if event.key == g.K_d:
            GameState.Player.rotateCW = True

    if event.type == g.KEYUP:
        if event.key == g.K_w:
            GameState.Player.thrusting = False

        if event.key == g.K_a:
            GameState.Player.rotateCCW = False
        
        if event.key == g.K_d:
            GameState.Player.rotateCW = False