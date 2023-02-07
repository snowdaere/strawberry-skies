import numpy as np

from GameState import GameState

class Entity:
    def __init__(self) -> None:
        self.pos = np.array((0, 0))
        self.size = 0.01
        self.renderpos = GameState.Camera.world2render(self.pos)
        self.rendersize = int(GameState.Camera.camzoom*(self.size))

    def update(self):
        self.renderpos = GameState.Camera.world2render(self.pos)
        pass

    def render(self):
        self.rendersize = GameState.Camera.camzoom*self.size
        pass