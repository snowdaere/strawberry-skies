import numpy as np
import math

import Rendering.Colors as Colors
import Entities.Sattelite as Sattelite

'''This code converts YAML into the solar system'''

def lcm(list:list):
    lcm = 1
    for i in list:
        lcm = math.lcm(lcm, i)
    return lcm

# Central System
Sun = Sattelite.Sattelite(Sattelite.Center, 0, 10, {'color': Colors.red, 'name':'Baal', 'Sun': True})
Planet1 = Sattelite.Sattelite(Sun, 10, 0.1, {'color': Colors.orange, 'name':'Paimon', 'Sun': False})
Planet2 = Sattelite.Sattelite(Sun, 20, 0.2, {'color': Colors.yellow, 'name':'Beleth', 'Sun': False})
Moon21 = Sattelite.Sattelite(Planet2, 2, 0.05, {'color': Colors.green, 'name':'Amdusius', 'Sun': False})
Moon22 = Sattelite.Sattelite(Planet2, 3, 0.05, {'color': Colors.brown, 'name':'Valefar', 'Sun': False})
Planet3 = Sattelite.Sattelite(Sun, 40, 0.3, {'color': Colors.green, 'name':'Purson', 'Sun': False})
Moon31 = Sattelite.Sattelite(Planet3, 2.5, 0.02, {'color': Colors.purple, 'name':'Agares', 'Sun': False})
Moon32 = Sattelite.Sattelite(Planet3, 3.5, 0.13, {'color': Colors.salmon, 'name':'Barbatos', 'Sun': False})
Moon33 = Sattelite.Sattelite(Planet3, 5, 0.01, {'color': Colors.orange, 'name':'Zepar', 'Sun': False})
Moon34 = Sattelite.Sattelite(Planet3, 7, 0.03, {'color': Colors.brown, 'name':'Aim', 'Sun': False})
Sattelite341 = Sattelite.Sattelite(Moon34, 1, 0.01, {'color': Colors.white, 'name':'Stolas', 'Sun': False})
Planet4 = Sattelite.Sattelite(Sun, 60, 0.6, {'color': Colors.blue, 'name':'Asmodeus', 'Sun': False})
Moon41 = Sattelite.Sattelite(Planet4, 1, 0.2, {'color': Colors.purple, 'name':'Astaroth', 'Sun': False})
Moon42 = Sattelite.Sattelite(Planet4, 1.5, 0.01, {'color': Colors.salmon, 'name':'Focalor', 'Sun': False})
Moon43 = Sattelite.Sattelite(Planet4, 3, 0.03, {'color': Colors.green, 'name':'Vepar', 'Sun': False})
Moon44 = Sattelite.Sattelite(Planet4, 3.5, 0.01, {'color': Colors.blue, 'name':'Crocell', 'Sun': False})
Moon45 = Sattelite.Sattelite(Planet4, 4, 0.02, {'color': Colors.white, 'name':'Allocer', 'Sun': False})
Moon46 = Sattelite.Sattelite(Planet4, 6, 0.13, {'color': Colors.yellow, 'name':'Murmur', 'Sun': False})
Sattelite461 = Sattelite.Sattelite(Moon46, 1, 0.01, {'color': Colors.brown, 'name':'Sytry', 'Sun': False})



System = [
    Sun,
    Planet1,
    Planet2,
    Moon21,
    Moon22,
    Planet3,
    Moon31,
    Moon32,
    Moon33,
    Moon34,
    Sattelite341,
    Planet4,
    Moon41,
    Moon42,
    Moon43,
    Moon44,
    Moon45,
    Moon46,
    Sattelite461,
]