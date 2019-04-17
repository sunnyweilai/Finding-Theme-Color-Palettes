"""
image quality assessment (IQA) of the quantized images and the original image in L*a*b* color space
----- method: PSNR
----- method: SSIM / version 1.0 (skimage library) / http://scikit-image.org/docs/dev/auto_examples/transform/plot_ssim.html
----- method: gmsd ("sporco" library) / reference:Gradient Magnitude Similarity Deviation: An Highly Efficient Perceptual Image Quality Index / https://arxiv.org/pdf/1308.3052.pdf
----- method: VIF / version 1.0 (VIF function written by Alex Izvorski) / https://github.com/aizvorski/video-quality/blob/master/vifp.py
"""
import numpy as np
from sklearn.cluster import KMeans
import scipy.misc
from skimage import color,data
from PIL import Image
import csv
import math
import sporco.metric
from skimage import color
from pandas.core.frame import DataFrame
from rgb_4IQAs import psnr_list,ssim_list,gmsd_list,vif_list





# ---- extract dominant color in the image
def kmeans_quantize(img, n_colors):
    ori_arr = np.array(img)
    width, height,depth = ori_arr.shape
    reshaped_raster = np.reshape(ori_arr, (width * height, depth))

    model = KMeans(n_clusters=n_colors,random_state = 1)
    labels = model.fit_predict(reshaped_raster)
    palette = model.cluster_centers_

    quantized_raster = np.reshape(
        palette[labels], (width, height, palette.shape[1]))
    # ---- rescale the quantized image to [0,1]
    rescale_quantized = quantized_raster / 255

    return rescale_quantized


def main() :
    # ---- open the reference image
    rgb_img = Image.open('../../../../img/img10.jpg')
    n_colors_list = range(1, 21)

    testimg_list = []
    for i in n_colors_list:
        result = kmeans_quantize(rgb_img, i)
        testimg_list.append(result)

    # ---- rescale the reference image into [0,1]
    rgb_raster = np.array(rgb_img)
    rescale_rgb_raster = rgb_raster / 255.0

    # ---- compute 4 IQAs
    PSNR_score_list = psnr_list(rescale_rgb_raster,testimg_list)
    SSIM_score_list = ssim_list(rescale_rgb_raster,testimg_list)
    VIF_score_list  = vif_list(rescale_rgb_raster,testimg_list)
    GMSD_score_list = gmsd_list(rescale_rgb_raster,testimg_list)

    # ----- build the framework and save csv
    score_dic = {"PSNR": PSNR_score_list, "SSIM": SSIM_score_list, "VIF": VIF_score_list, "GMSD": GMSD_score_list}
    score_table = DataFrame(score_dic)
    score_table.to_csv('rgb_results/10score_table.csv')




if __name__ == "__main__":
    main()

