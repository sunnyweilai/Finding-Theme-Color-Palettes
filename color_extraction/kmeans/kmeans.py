import numpy as np
from sklearn.cluster import KMeans
from sklearn.datasets import load_sample_image
from sklearn import metrics
import scipy.misc
import matplotlib.pyplot as plt

from PIL import Image


# def loaddata(picpath):
#     image = Image.open(picpath)
#     width,height = image.size
#     pixdata = []
#     r, g, b = image.split()
#     pixdata.append(r, g, b)
#
#     return np.mat(pixdata), width, height



def quantize(picpath, n_colors):
    # image = load_sample_image(picpath)
    # image = np.array(image, dtype=np.float64) / 255
    #
    raster = scipy.misc.imread(picpath)
    width, height, depth = raster.shape
    # width,height, depth = original_shape = tuple(image.shape)
    # assert depth == 3
    # image_arrary = np.reshape(image,(width*))
    reshape_pic = np.reshape(raster, (width * height, depth))

    model = KMeans(n_clusters = n_colors, random_state = 0)
    labels = model.fit_predict(reshape_pic)
    palette = model.cluster_centers_

    quantized_pic = np.reshape(
        palette[labels], (width, height, palette.shape[1])
    )
    """
    reshape the picture based on the color theme (5 colors)
    score function gives the sum of all distances between the sample data and their associated clusters
    large distances if you have a big variety of data samples
    """
    reshape_quantized_pic = np.reshape(reshape_pic,(width * height,depth))
    score = model.score(reshape_quantized_pic)
    cali_score = metrics.calinski_harabaz_score(reshape_pic, labels)
    return score, cali_score, quantized_pic

result = quantize('img/universe.jpg', 5)
print(result)
# result = -2841350551.99,which means sample data has a big variety




#
# image = np.array(Image.open('img/universe.jpg'))
# kmeansed_pic = quantize(image,5)
# kmeansed_pic.save('kmeans_pic.png')
# print(loaddata('img/universe.jpg'))

# plt.imshow(palette, cmap=plt.cm.binary)
# plt.show()