"""
image quality assessment (IQA) of the quantized images and the original image in RGB color space
----- method: PSNR
----- version 1.0 ("skimage" library)
----- http://scikit-image.org/docs/dev/api/skimage.measure.html#skimage.measure.compare_psnr
"""

import numpy as np
from PIL import Image
import glob
import csv
import skimage.measure as skm


# ---- obtain the original and quantized images
temp_img = np.array(Image.open('../../../../img/sky.jpg'))
quantized_img_path_list = []
quantized_img_path_list = glob.glob(r'../../../img/sky/rgb_cs/quantized_img/*.png')
quantized_img_path_list.sort()

# ---- compute PSNR
score_list = []
for i in quantized_img_path_list:
    quantized_img = np.array(Image.open(i))
    score = skm.compare_psnr(temp_img, quantized_img)
    score_list.append(score)
# print(score_list)


# ---- save psnr score to csv file
csvfile = "sky_psnr.csv"
with open(csvfile, "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    for val in score_list:
        writer.writerow([val])