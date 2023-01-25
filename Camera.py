import numpy as np

## CAMERA CODE
# initialize the camera settings
# is the scale setting, or how many display pixels make a game unit
camzoomdefault = 100
camzoom = camzoomdefault
campos = camx, camy = np.array((0, 0))

camzoommin = 0.0625*camzoomdefault
camzoommax = 4*camzoomdefault

# this object is used to flip the screen coordinates to a standard x/y orientation
flip1 = np.array((1, -1))
flip2 = np.array((-1, 1))
# Says whether the game is panning or not (to update the campos)
Dragging = False
# dummy variable used for holding offset while panning
PanStartPos = np.array((0, 0))
CamPosStart = np.array((0, 0))
CamPosOffset = np.array((0, 0))

## GENERAL GAME ESTABLISHMENT
# define game variables
dim = width, height = np.array((800, 800))
# the center vector points from the corner of the screen to the middle
center = np.array((width/2, height/2))