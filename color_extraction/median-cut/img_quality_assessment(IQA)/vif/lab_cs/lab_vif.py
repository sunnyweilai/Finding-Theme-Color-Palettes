"""
image quality assessment (IQA) of the quantized images and the original image in L*a*b* color space
----- method: VIF
----- version 1.0 (VIF function written by Alex Izvorski)
----- https://github.com/aizvorski/video-quality/blob/master/vifp.py
"""
from PIL import Image
import skimage
from quantization import median_cut
import numpy as np
import csv
from vif_function import vifp_mscale


def main() :
    # ---- open the reference image
    original_img = Image.open('../../../../img/sky.jpg')

    # do the median-cut
    testimg_list = []
    for n_colors in range(1, 21):
        lab_array = median_cut(original_img, n_colors)
        testimg_list.append(lab_array)

    # ---- get lab original array
    ori_arr = np.array(original_img)
    ori_arr_lab = skimage.color.rgb2lab(ori_arr)

    # ---- rescale original raster to [0,1]
    rescale_ori = (ori_arr_lab + [0, 128, 128]) / [100, 255, 255]

    # ---- compute VIF
    score_list = []
    for i in testimg_list:
        score = vifp_mscale(rescale_ori, i)
        score_list.append(score)

    # ---- save vif score to csv file
    csvfile = "lab_sky_vif.csv"
    with open(csvfile, "w") as output:
        writer = csv.writer(output, lineterminator='\n')
        for val in score_list:
            writer.writerow([val])

if __name__ == "__main__":
    main()
