# -*- coding: UTF-8 -*-
import numpy as np
import pandas as pd
import scipy as sp
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cm as cmx
from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns
from PIL import Image
from skimage import io


img = Image.open('img/universe.jpg')

# io.imshow(img)
# io.show()

# ----build RGB list
# https://www.zhihu.com/question/29807693
pix = img.load()
width = img.size[0]
height = img.size[1]
img = img.convert('RGB')
rgb_array = []
for x in range(width):
    for y in range(height):
        r, g, b = pix[x,y]
        rgb = (r, g, b)
        rgb_array.append(rgb)
# print(rgb_array)


# ----build dataframe
component_distribution = pd.DataFrame(rgb_array, columns=['Red', 'Green', 'Blue'])
print(component_distribution)

# draw 3d rgb distribution
cm = plt.get_cmap("RdYlGn")
x, y, z = component_distribution['Red'],component_distribution['Green'],component_distribution['Blue']
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')  # 创建一个三维的绘图工程
#  将数据点分成三部分画，在颜色上有区分度
ax.scatter(x,y,z,cmap= cm)  # 绘制数据点
ax.set_zlabel('Red')  # 坐标轴
ax.set_ylabel('Green')
ax.set_xlabel('Blue')
plt.show()

# def scatter3d(x,y,z, cs, colorsMap='jet'):
#     cm = plt.get_cmap(colorsMap)
#     cNorm = matplotlib.colors.Normalize(vmin=min(cs), vmax=max(cs))
#     scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=cm)
#     fig = plt.figure()
#     ax = Axes3D(fig)
#     ax.scatter(x, y, z, c=scalarMap.to_rgba(cs))
#     ax.set_zlabel('Red')  # 坐标轴
#     ax.set_ylabel('Green')
#     ax.set_xlabel('Blue')
#     scalarMap.set_array(cs)
#     fig.colorbar(scalarMap)
#     plt.show()
#
# scatter3d(x,y,z, cs, colorsMap='jet')