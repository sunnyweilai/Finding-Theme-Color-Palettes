import numpy as np
import cv2
import colorsys
import skimage
from skimage import io
from sklearn.cluster import KMeans
from sklearn.datasets import load_sample_image
from sklearn import metrics
import scipy.misc
import matplotlib.pyplot as plt
import  matplotlib.colors as mcolors
from PIL import Image,ImageCms
from sklearn.metrics import pairwise_distances_argmin
from sklearn.utils import shuffle
from skimage import color


# convert to lab color space to do kmeans
rgb_raster = scipy.misc.imread('../img/sky.jpg')
lab_raster = color.rgb2lab(rgb_raster)

# extract dominant colot in the image
def quantize(raster, n_colors):
    width, height,depth = raster.shape
    reshaped_raster = np.reshape(raster, (width * height, depth))

    model = KMeans(n_clusters=n_colors,random_state = 1)
    labels = model.fit_predict(reshaped_raster)
    palette = model.cluster_centers_

    quantized_raster = np.reshape(
        palette[labels], (width, height, palette.shape[1]))

    # convert back to rgb model to save new image
    new_rgb_raster = color.lab2rgb(quantized_raster) * 255
    quantized_image = Image.fromarray(new_rgb_raster.astype(np.uint8))
    quantized_image.save("img/sky/lab_cs/quantized_img/img_quantized%02d.png" % n_colors)
    # return quantized_raster


n_colors_list = [5]
for i in n_colors_list:
    result = quantize(lab_raster, i)











# visualize lab image
# rgb_image = color.lab2rgb(lab_quantize)
# plt.imshow(rgb_image)
# plt.draw()
# plt.show()




# normalize lab colorspace into [0:1]
# l,a,b = cv2.split(lab_quantize)
# l = l / 100
# a = (a + 86.185) / 184.439
# b = (b + 107.863) / 202.345
# lab_image = cv2.merge((l,a,b))
# print(lab_image)
# lab_image = (lab_quantize + [0, 128, 128]) / [100, 255, 255]
# lab_image = Image.fromarray(lab_quantize.astype(float))
# print(lab_image)
# with skimage.external.tifffile.TiffWriter('temp.tif', bigtiff=True) as tif:
#     for i in range(lab_quantize.shape[0]):
#         tif.save(lab_quantize[i], compress=6, photometric='lab' )

# skimage.external.tifffile.imsave('lab.tif',lab_image)
# print(lab_quantize.dtype.name)



# # normalize lab colorspace into [0:1]
# l,a,b = cv2.split(lab_quantize)
# l = l / 100
# a = (a + 86.185) / 184.439
# b = (b + 107.863) / 202.345
# lab_image = cv2.merge((l,a,b))
#
# # cv2.imshow('image', lab)
# # cv2.waitKey(0)
# # cv2.destroyAllWindows()
#
