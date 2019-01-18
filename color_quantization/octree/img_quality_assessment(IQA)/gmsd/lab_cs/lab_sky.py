"""
image quality assessment (IQA) of the quantized images and the original image in L*a*b* color space
----- version 1.0 method: gmsd ("sporco" library)
----- reference:Gradient Magnitude Similarity Deviation: An Highly Efficient Perceptual Image Quality Index
----- https://arxiv.org/pdf/1308.3052.pdf
"""

import scipy.misc
import glob
import csv
import sporco.metric
from skimage import color

# ---- get the original image array
temp_img = scipy.misc.imread('../../../../img/sky.jpg')

# ---- convert the original image from RGB into L*a*b* color space
lab_temp_img = (color.rgb2lab(temp_img) + [0, 128, 128]) / [100, 255, 255]
lab_temp_width = lab_temp_img.shape[0]
lab_temp_height = lab_temp_img.shape[1]*lab_temp_img.shape[2]

# ---- resize the original image array into 2d in order to the computation
lab_temp_img.resize((lab_temp_width,lab_temp_height))

# ---- get all the quantized images from the folder
quantized_img_path_list = []
quantized_img_path_list = glob.glob(r'../../../img/sky/lab_cs/quantized_img/*.png')
quantized_img_path_list.sort()


score_list = []
for i in quantized_img_path_list:
    quantized_img = scipy.misc.imread(i)

    # ---- convert the quantized image from RGB into L*a*b* color space
    lab_quantized_img = (color.rgb2lab(quantized_img)+ [0, 128, 128]) / [100, 255, 255]
    lab_quantized_width = lab_quantized_img.shape[0]
    lab_quantized_height = lab_quantized_img.shape[1]*lab_quantized_img.shape[2]
    lab_quantized_img.resize((lab_quantized_width,lab_quantized_height))

    # ---- compute gmsd
    score = sporco.metric.gmsd(lab_temp_img, lab_quantized_img)
    score_list.append(score)
print(score_list)

# ---- save gmsd score to csv file
csvfile = "sky_gmsd.csv"
with open(csvfile, "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    for val in score_list:
        writer.writerow([val])