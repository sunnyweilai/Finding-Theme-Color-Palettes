import numpy as np
from sklearn.cluster import KMeans
from sklearn.datasets import load_sample_image
from sklearn import metrics
import scipy.misc
import matplotlib.pyplot as plt
import  matplotlib.colors as mcolors
from gensim.models.coherencemodel import CoherenceModel
from gensim.corpora.dictionary import Dictionary

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
    raster = scipy.misc.imread(picpath)
    width, height, depth = raster.shape

    reshape_raster = np.reshape(raster, (width * height, depth))

    model = KMeans(n_clusters = n_colors, random_state = 1)
    labels = model.fit_predict(reshape_raster)
    palette = model.cluster_centers_

    # reshape the picture based on the color theme (n colors)
    quantized_raster = np.reshape(
        palette[labels], (width, height, palette.shape[1])
    )

    # save quantized_img and colortheme_palette
    image = Image.fromarray(quantized_raster.astype(np.uint8))
    image.save("img/universe/quantized_img/img_quantized%s.png" % n_colors)

    rgb_palette = palette / 255.0
    img_palette = mcolors.ListedColormap(rgb_palette)
    plt.figure(figsize=(n_colors, 0.5))
    plt.title('color theme')
    plt.pcolormesh(np.arange(img_palette.N).reshape(1, -1), cmap=img_palette)
    plt.gca().yaxis.set_visible(False)
    plt.gca().set_xlim(0, img_palette.N)
    # plt.show()
    plt.savefig('img/universe/quantized_palette/img_palette%s.png' % n_colors)

    """
    use 2 validation methods to know how many numbers of colors in color theme is the best
    score, calinski-marabasez
    """
    scores_for_each = []
    # score function gives the sum of all distances between the sample data and their associated clusters
    # large distances if you have a big variety of data samples
    score = model.score(palette[labels])

    # Calinski-Harabasz score
    cali_score = metrics.calinski_harabaz_score(reshape_raster, labels)

    scores_for_each.extend((score, cali_score))

    # # coherencemodel
    # dictionary = Dictionary(palette[labels])
    # corpus = palette[labels]
    # cm = CoherenceModel(topics=palette, dictionary=dictionary, corpus=corpus, coherence='u_mass')
    # co = cm.get_coherence()

    return scores_for_each

n_colors_list = [15,20]

for i in n_colors_list:
    result = quantize('../img/universe.jpg', i)
    print(result)







# ---------------------find the number of different colors in the image
# img = Image.open('../img/universe.jpg')
# pix = img.load()
# width = img.size[0]
# height = img.size[1]
# img = img.convert('RGB')
# rgb_array = []
# for x in range(width):
#     for y in range(height):
#         r, g, b = pix[x,y]
#         rgb = (r,g,b)
#         # rgb = (int(str(r) + str(g) + str(b)))
#         rgb_array.append(rgb)
# print(len(rgb_array))
# a = set(rgb_array)
# print(len(a))


