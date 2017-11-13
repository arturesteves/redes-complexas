import matplotlib.pyplot as plt

import numpy as np
import matplotlib.pyplot as plt

t = np.arange(0., 5., 0.2)
print t
print t[1]

# evenly sampled time at 200ms intervals
t = [[[0.0, 345, 1000, 3, 0.003], [0.2, 998, 1000, 997, 0.997], [0.4, 999, 1000, 999, 0.999], [0.6, 999, 1000, 999, 0.999], [0.8, 999, 1000, 999, 0.999], [1.0, 999, 1000, 999, 0.999]], [[0.0, 260, 1000, 21, 0.021], [0.2, 502, 1000, 43, 0.043], [0.4, 542, 1000, 53, 0.053], [0.6, 547, 1000, 266, 0.266], [0.8, 938, 1000, 915, 0.915], [1.0, 975, 1000, 963, 0.963]], [[0.0, 260, 1000, 21, 0.021], [0.2, 502, 1000, 43, 0.043], [0.4, 542, 1000, 53, 0.053], [0.6, 547, 1000, 266, 0.266], [0.8, 938, 1000, 915, 0.915], [1.0, 975, 1000, 963, 0.963]]]
x_list = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
y_list1 = map(lambda v: v[4], t[0])
y_list2 = map(lambda v: v[4], t[1])
y_list3 = map(lambda v: v[4], t[2])

print x_list
print y_list1
# red dashes, blue squares and green triangles
plt.plot(x_list, y_list1, 'r--', x_list, y_list2, 'bs--', x_list, y_list3, 'g^--')
plt.show()

