"""
Using kmeans algorithm from "sklearn" library to extract color themes (1-20) from the "sky" image in L*a*b* color space
----reference: https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html
"""
import numpy as np
import skimage
from sklearn.cluster import KMeans
from sklearn.datasets import load_sample_image
from sklearn import metrics
import scipy.misc
import matplotlib.pyplot as plt
import  matplotlib.colors as mcolors
from PIL import Image,ImageCms
from skimage import color
# get the run time
import datetime


# start timer
start = datetime.datetime.now()
# ---- convert the image from rgb to lab color space
rgb_raster = scipy.misc.imread('../img/img10.jpg')
lab_raster = color.rgb2lab(rgb_raster)

# ---- extract dominant color in the image
def quantize(raster, n_colors):
    width, height,depth = raster.shape
    reshaped_raster = np.reshape(raster, (width * height, depth))

    model = KMeans(n_clusters=n_colors,random_state = 1)
    labels = model.fit_predict(reshaped_raster)
    palette = model.cluster_centers_

    # ------- reshape the picture based on the color theme (n colors)
    # ------- reference: "color quantization using kmeans" writtern by Lou Marvin Caraig
    # ------- https://lmcaraig.com/color-quantization-using-k-means/#usingkmeansinrgbspace
    quantized_raster = np.reshape(
        palette[labels], (width, height, palette.shape[1]))

    # ---- convert back to rgb model to save new image
    new_rgb_raster = color.lab2rgb(quantized_raster) * 255
    quantized_image = Image.fromarray(new_rgb_raster.astype(np.uint8))
    quantized_image.save("img/img10/lab_cs/quantized_img/img_quantized%02d.png" % n_colors)

    # ---- transform to 3d array to do the color space conversion
    lab_array = np.asarray([palette])
    new_lab_palette = lab_array.astype(float)
    back2rgb_palette = skimage.color.lab2rgb(new_lab_palette)

    # ---- transform back to 2d array in order to do the palette visualization
    rgb_palette = []
    for rgb in back2rgb_palette[0]:
        rgb_palette.append(rgb)

    # ---- visualize and save color theme palettes
    img_palette = mcolors.ListedColormap(rgb_palette)
    plt.figure(figsize=(n_colors, 0.5))
    plt.title('color theme')
    plt.pcolormesh(np.arange(img_palette.N).reshape(1, -1), cmap=img_palette)
    plt.gca().yaxis.set_visible(False)
    plt.gca().set_xlim(0, img_palette.N)
    plt.axis('off')
    plt.savefig('img/img10/lab_cs/quantized_palette/img_palette%02d.png' % n_colors)


for i in range(1,21):
    quantize(lab_raster, i)
end = datetime.datetime.now()
print (end-start)


