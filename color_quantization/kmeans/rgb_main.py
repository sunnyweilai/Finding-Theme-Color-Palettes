"""
Using kmeans algorithm from "sklearn" library to extract color themes (1-20) from the "sky" image in RGB color space
reference: https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html
"""
import numpy as np
from sklearn.cluster import KMeans
from sklearn.datasets import load_sample_image
from sklearn import metrics
import scipy.misc
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from PIL import Image
# get the run time
import datetime



def quantize(raster, n_colors):
    # ---- raster image into rgb color space
    width, height, depth = raster.shape
    reshape_raster = np.reshape(raster, (width * height, depth))

    # ---- create kmeans model
    model = KMeans(n_clusters = n_colors, random_state = 1)
    labels = model.fit_predict(reshape_raster)
    palette = model.cluster_centers_

    # ------- reshape the picture based on the color theme (n colors)
    # ------- reference: "color quantization using kmeans" writtern by Lou Marvin Caraig
    # ------- https://lmcaraig.com/color-quantization-using-k-means/#usingkmeansinrgbspace
    quantized_raster = np.reshape(
        palette[labels], (width, height, palette.shape[1])
    )

    # ---- save quantized images
    image = Image.fromarray(quantized_raster.astype(np.uint8))
    image.save("img/img10/rgb_cs/quantized_img/img_quantized%02d.png" % n_colors)

    # ---- visualize and save color theme palettes
    rgb_palette = palette / 255.0
    img_palette = mcolors.ListedColormap(rgb_palette)
    plt.figure(figsize=(n_colors, 0.5))
    plt.title('color theme')
    plt.pcolormesh(np.arange(img_palette.N).reshape(1, -1), cmap=img_palette)
    plt.gca().yaxis.set_visible(False)
    plt.gca().set_xlim(0, img_palette.N)
    plt.axis('off')
    plt.savefig('img/img10/rgb_cs/quantized_palette/img_palette%02d.png' % n_colors)

# start timer
start = datetime.datetime.now()


rgb_raster = scipy.misc.imread('../img/img10.jpg')
for i in range(5,21):
    quantize(rgb_raster, i)
# end timer
end = datetime.datetime.now()
print (end-start)



