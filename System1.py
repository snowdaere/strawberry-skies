from main import Body, Sattelite
import numpy as np
from dotmap import DotMap
import Colors



Sun = Body(np.array((0, 0)), 10, {'color': Colors.yellow, 'name':'Sun'})
Planet1 = Sattelite(Sun, 5, 1, {'color': Colors.green, 'name':'Foo'})
Planet2 = Sattelite(Sun, 10, 0.5, {'color': Colors.blue, 'name':'Bar'})
Planet3 = Sattelite(Sun, 30, 5, {'color': Colors.orange, 'name':'Barry'})

System = [Sun, Planet1, Planet2, Planet3]