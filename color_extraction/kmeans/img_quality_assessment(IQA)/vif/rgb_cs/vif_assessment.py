"""
image quality assessment (IQA) of the quantized images and the original image in RGB color space
----- method: VIF
----- version 1.0 (VIF function written by Alex Izvorski)
----- https://github.com/aizvorski/video-quality/blob/master/vifp.py
"""


import numpy as np
from PIL import Image
import glob
import csv
from vif_function import vifp_mscale

# ---- obtain the original and quantized image arrays
temp_img = np.array(Image.open('../../../../img/sky.jpg'),'f')
quantized_img_path_list = []
quantized_img_path_list = glob.glob(r'../../../img/sky/rgb_cs/quantized_img/*.png')
quantized_img_path_list.sort()


score_list = []
for i in quantized_img_path_list:
    quantized_img = np.array(Image.open(i),'f')
    score = vifp_mscale(temp_img, quantized_img)
    score_list.append(score)
print(score_list)

# ---- save vif score to csv file
csvfile = "sky_vif.csv"
with open(csvfile, "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    for val in score_list:
        writer.writerow([val])