import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

x_points = [0,0,0,1,1,0,-1]
y_points = [0,1,2,2,3,3,3]

colors = []
colors.append((0,0,1))
colors.append((1,0,0))
colors.append((1,0,0))
colors.append((0,0,1))
colors.append((1,0,0))
colors.append((1,0,0))
colors.append((0,0,1))

fig, ax = plt.subplots()
plt.plot(x_points, y_points, linestyle='-', color='black', linewidth=3, zorder=0)
plt.scatter(x_points, y_points, c = colors, s = 200, zorder=10)

plt.plot((0,0), (2,3), linestyle=':', color=(1,0,0))

ax.xaxis.set_major_locator(plt.MultipleLocator(1))
ax.yaxis.set_major_locator(plt.MultipleLocator(1))
plt.axis("equal")
plt.grid()
plt.show()
