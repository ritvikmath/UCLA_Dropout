import numpy as np
import math

x = 50

while(abs(x) > 0.01)
	x = x - math.sinh(x)
	
print x