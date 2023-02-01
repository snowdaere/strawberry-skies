import numpy as np
import math

import Rendering.Colors as Colors
import Entities.Body as Body
import Entities.Sattelite as Sattelite

'''This code converts YAML into the solar system'''

def lcm(list:list):
    lcm = 1
    for i in list:
        lcm = math.lcm(lcm, i)
    return lcm

# Central System
Sun = Body.Body(np.array((0, 0)), 10, {'color': Colors.yellow, 'name':'Sun', 'Sun': True})

Planet1 = Sattelite.Sattelite(Sun, 5, 1, {'color': Colors.green, 'name':'Foo', 'Sun': False})
Moon1 = Sattelite.Sattelite(Planet1, 1, 0.1, {'color': Colors.brown, 'name':'Moo', 'Sun': False})

Planet2 = Sattelite.Sattelite(Sun, 10, 0.5, {'color': Colors.blue, 'name':'Bar', 'Sun': False})

Planet3 = Sattelite.Sattelite(Sun, 30, 5, {'color': Colors.orange, 'name':'Barry', 'Sun': False})
Moon2 = Sattelite.Sattelite(Planet3, 5, 0.2, {'color': Colors.green, 'name':'Barrys Son', 'Sun': False})
Moon3 = Sattelite.Sattelite(Planet3, 4, 0.13, {'color': Colors.salmon, 'name':'Barrys other Son', 'Sun': False})
Moon4 = Sattelite.Sattelite(Moon2, 0.5, 0.1, {'color': Colors.green, 'name':'Barrys Sons Son', 'Sun': False})




System = [Sun, Planet1, Planet2, Planet3, Moon1, Moon2, Moon3, Moon4]