import numpy as np
import pygame as g

## CAMERA CODE
# initialize the camera settings
# is the scale setting, or how many display pixels make a game unit
camzoomdefault:float = 100
camzoom:float = camzoomdefault
campos = camx, camy = np.array((0, 0))

camzoommin = 0.5*0.0625*camzoomdefault
camzoommax = 4*camzoomdefault

# this object is used to flip the screen coordinates to a standard x/y orientation
flip1 = np.array((1, -1))
flip2 = np.array((-1, 1))
# Says whether the game is panning or not (to update the campos)
Dragging = False
# is the game following the ship?
Follow = True
# dummy variable used for holding offset while panning
PanStartPos = np.array((0, 0))
CamPosStart = np.array((0, 0))
CamPosOffset = np.array((0, 0))

## GENERAL GAME ESTABLISHMENT
# define game variables
dim = width, height = np.array((1920, 1080))
# the center vector points from the corner of the screen to the middle
center = np.array((width/2, height/2))

def render2world(renderpos:np.array):
    '''Transforms camera coordinates to in-world coordinates'''
    return flip1*((1/camzoom)*(renderpos - center) - flip2*campos)

def world2render(worldpos:np.array):
    '''Transforms in-world coordinates to camera coordinates'''
    return center + camzoom*(flip2*campos + flip1*worldpos)

def mouse():
    '''gets mouse position as a vector'''
    return np.array(g.mouse.get_pos())

def zoomout():
    '''zooms out'''
    global camzoom
    if camzoom > camzoommin:
        camzoom *= 0.5

def zoomin():
    '''zooms in'''
    global camzoom
    if camzoom < camzoommax:
        camzoom *= 2