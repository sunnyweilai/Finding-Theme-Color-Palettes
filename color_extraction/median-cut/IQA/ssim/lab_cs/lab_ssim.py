import numpy as np
import csv
from PIL import Image
import skimage
import math
from sklearn.cluster import KMeans
import scipy.misc
from skimage import color,data,img_as_uint
from skimage.measure import compare_ssim
from quantization import median_cut


def main() :
    # open the reference image
    original_img = Image.open('../../../../img/sky.jpg')

    testimg_list = []
    for n_colors in range(1, 21):
        lab_array = median_cut(original_img, n_colors)
        testimg_list.append(lab_array)

    #get lab original array
    ori_arr = np.array(original_img)
    ori_arr_lab = skimage.color.rgb2lab(ori_arr)

    # rescale original raster
    rescale_ori = (ori_arr_lab + [0, 128, 128]) / [100, 255, 255]

    # compare MSSIM
    score_list = []
    for i in testimg_list:
        score = compare_ssim(rescale_ori, i, multichannel=True)
        score_list.append(score)

    # save ssim score to csv file
    csvfile = "added_L_ssim_lab.csv"
    with open(csvfile, "w") as output:
        writer = csv.writer(output, lineterminator='\n')
        for val in score_list:
            writer.writerow([val])

if __name__ == "__main__":
    main()
