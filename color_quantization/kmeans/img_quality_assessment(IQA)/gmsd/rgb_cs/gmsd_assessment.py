"""
image quality assessment (IQA) of the quantized images and the original image in RGB color space
----- method: gmsd ("sporco" library)
----- reference:Gradient Magnitude Similarity Deviation: An Highly Efficient Perceptual Image Quality Index
----- https://arxiv.org/pdf/1308.3052.pdf
"""

import numpy as np
from PIL import Image
import glob
import csv
import math
import sporco.metric

# ---- resize the original image array into 2d
temp_img = np.array(Image.open('../../../../img/img10.jpg'),'f')
temp_width = temp_img.shape[0]
temp_height = temp_img.shape[1]*temp_img.shape[2]
temp_img.resize((temp_width,temp_height))

# ---- get all the quantized images from the folder
quantized_img_path_list = []
quantized_img_path_list = glob.glob(r'../../../img/img10/rgb_cs/quantized_img/*.png')
quantized_img_path_list.sort()

# ---- compute gmsd
score_list = []
for i in quantized_img_path_list:
    quantized_img = np.array(Image.open(i),'f')
    quantized_width = quantized_img.shape[0]
    quantized_height = quantized_img.shape[1]*quantized_img.shape[2]
    quantized_img.resize((quantized_width,quantized_height))
    score = sporco.metric.gmsd(temp_img, quantized_img)
    score_list.append(score)
# print(score_list)

# ---- save gmsd score to csv file
csvfile = "img10_gmsd.csv"
with open(csvfile, "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    for val in score_list:
        writer.writerow([val])