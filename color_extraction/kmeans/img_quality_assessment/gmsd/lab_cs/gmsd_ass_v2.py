import numpy as np
import scipy.misc
from PIL import Image
import glob
import csv
import math
import sporco.metric
from skimage import color


temp_img = scipy.misc.imread('../../../../img/sky.jpg')
lab_temp_img = (color.rgb2lab(temp_img) + [0, 128, 128]) / [100, 255, 255]
print(lab_temp_img)
lab_temp_width = lab_temp_img.shape[0]
lab_temp_height = lab_temp_img.shape[1]*lab_temp_img.shape[2]
lab_temp_img.resize((lab_temp_width,lab_temp_height)) #resize array to 2d


quantized_img_path_list = []
quantized_img_path_list = glob.glob(r'../../../img/sky/lab_cs/quantized_img/*.png')
quantized_img_path_list.sort()

score_list = []
for i in quantized_img_path_list:
    quantized_img = scipy.misc.imread(i)
    lab_quantized_img = (color.rgb2lab(quantized_img)+ [0, 128, 128]) / [100, 255, 255]
    lab_quantized_width = lab_quantized_img.shape[0]
    lab_quantized_height = lab_quantized_img.shape[1]*lab_quantized_img.shape[2]
    lab_quantized_img.resize((lab_quantized_width,lab_quantized_height))
    score = sporco.metric.gmsd(lab_temp_img, lab_quantized_img)
    score_list.append(score)
print(score_list)

# save gmsd score to csv file
csvfile = "lab_sky_gmsd.csv"
with open(csvfile, "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    for val in score_list:
        writer.writerow([val])