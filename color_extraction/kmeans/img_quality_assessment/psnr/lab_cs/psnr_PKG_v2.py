import numpy as np
import scipy.misc
from PIL import Image
import glob
import csv
import math
import skimage.measure as skm
from skimage import color




temp_img = scipy.misc.imread('../../../../img/sky.jpg')
lab_temp_img = color.rgb2lab(temp_img)
quantized_img_path_list = []
quantized_img_path_list = glob.glob(r'../../../img/sky/lab_cs/quantized_img/*.png')
quantized_img_path_list.sort()


score_list = []
for i in quantized_img_path_list:
    quantized_img = scipy.misc.imread(i)
    score = skm.compare_psnr(temp_img, quantized_img)
    score_list.append(score)
# print(score_list)


# save psnr score to csv file
csvfile = "lab_sky_psnr.csv"
with open(csvfile, "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    for val in score_list:
        writer.writerow([val])