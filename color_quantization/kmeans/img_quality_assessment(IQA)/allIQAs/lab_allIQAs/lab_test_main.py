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
from lab_4IQAs import psnr_list,ssim_list,gmsd_list,vif_list
from pandas.core.frame import DataFrame
import skimage
import os.path



def open_pics(path_pics):
    files =os.listdir(path_pics)
    files.sort()
    pic_list = []
    for file in files:
        if file.endswith('jpg'):
            new_path = path_pics + '/' + str(file)
            pic_list.append((int(str(file)[:2]),new_path))
    return pic_list





# ---- extract dominant color in the image
def kmeans_quantize(img, n_colors):

    # ---- convert the RGB array of the original image into L*a*b* color space
    ori_arr = np.array(img)
    ori_arr_lab = skimage.color.rgb2lab(ori_arr)
    width, height,depth = ori_arr_lab.shape
    reshaped_raster = np.reshape(ori_arr_lab, (width * height, depth))

    model = KMeans(n_clusters=n_colors,random_state = 1)
    labels = model.fit_predict(reshaped_raster)
    palette = model.cluster_centers_

    quantized_raster = np.reshape(
        palette[labels], (width, height, palette.shape[1]))

    # rescale float to [0,1]
    rescale_quant = (quantized_raster + [0, 128, 128]) / [100, 255, 255]
    return rescale_quant


def main():
    path_pics = '../../../../img/test_image'
    pic_list = open_pics(path_pics)
    for pic_nam, pic_path in pic_list:
        # ---- open the reference image
        rgb_img = Image.open(pic_path)
        n_colors_list = range(1, 21)

        testimg_list = []
        for i in n_colors_list:
            result = kmeans_quantize(rgb_img, i)
            testimg_list.append(result)

        # ---- rescale the reference image into [0,1]
        rgb_raster = np.array(rgb_img)
        lab_raster = skimage.color.rgb2lab(rgb_raster)
        rescale_lab_raster = (lab_raster + [0, 128, 128]) / [100, 255, 255]

        # ---- compute 4 IQAs
        PSNR_score_list, L_PSNR_score_list = psnr_list(rescale_lab_raster, testimg_list)
        SSIM_score_list, L_SSIM_score_list = ssim_list(rescale_lab_raster, testimg_list)
        VIF_score_list = vif_list(rescale_lab_raster, testimg_list)
        GMSD_score_list = gmsd_list(rescale_lab_raster, testimg_list)

        # ----- build the framework and save csv
        score_dic = {"PSNR": PSNR_score_list, "SSIM": SSIM_score_list, "VIF": VIF_score_list, "GMSD": GMSD_score_list}
        score_table = DataFrame(score_dic)
        score_table.to_csv('lab_results/lab_50/%02dscore_table.csv' % pic_nam)

        # ----  build L* and lab framework
        l_score_dic = {"PSNR": PSNR_score_list, "L_PSNR": L_PSNR_score_list, "SSIM": SSIM_score_list,
                       "L_SSIM": L_SSIM_score_list}
        l_score_table = DataFrame(l_score_dic)

        l_score_table.to_csv('lab_results/L_compare_50/%02d_L_score.csv' % pic_nam)


if __name__ == "__main__":
    main()
