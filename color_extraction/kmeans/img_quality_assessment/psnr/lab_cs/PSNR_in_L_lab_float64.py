import numpy as np
import csv
import cv2
from sklearn.cluster import KMeans
import scipy.misc

import sys
sys.path.insert(0, '/anaconda2/envs/Lai_Project/color_extraction/kmeans/img_quality_assessment/psnr/lab_cs')

from quantization_sky_float64 import testimg_list, rescale_ori, psnr
# from color_extraction.kmeans.quantization_sky import testimg_list, rescale_ori, psnr


# seperate L* channel of the original image
L_ori = rescale_ori[:,:,0]


# compare PSNR
score_list = []
for i in testimg_list:
    score = psnr(L_ori, i[:,:,0])
    score_list.append(score)
print(score_list)

# save PSNR score to csv file
csvfile = "psnr_lab_v3.csv"
with open(csvfile, "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    for val in score_list:
        writer.writerow([val])









