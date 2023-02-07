import pygame as g

from Rendering.Camera import Camera
import Rendering.Colors as Colors


# Says what screen the game is in
class GameState:
    MainScreen = True
    Paused = False
    FPS = 60
    running = True
    # physics time step in s
    dt = 1/60
    # Define universal constants
    # gravitational constant
    G = 0.1
    # define game time
    t = 0

    # initialize the game stuff
    flags = g.HWSURFACE | g.FULLSCREEN | g.DOUBLEBUF
    display = g.display.set_mode(Camera.dim, flags, vsync=1)
    g.display.set_caption('Strawberry Skies')
    clock = g.time.Clock()
    display.fill(Colors.black)

    # initialize fint
    g.font.init()
    font = g.font.SysFont('Courier', 20)

    # set icon
    gameicon = g.image.load('Assets/strawberry.png')
    g.display.set_icon(gameicon)

    Bodies = []
    Entities = []
    Player = None
    Camera = None