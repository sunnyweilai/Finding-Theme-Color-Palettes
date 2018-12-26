import numpy as np
import scipy.misc
from PIL import Image
import glob
import csv
import math
import sporco.metric


temp_img = np.array(Image.open('temp_image.png'),'f')
temp_width = temp_img.shape[0]
temp_height = temp_img.shape[1]*temp_img.shape[2]
temp_img.resize((temp_width,temp_height)) #resize array to 2d


quantized_img_path_list = []
quantized_img_path_list = glob.glob(r'../../../img/sky/lab_cs/quantized_img/*.png')
quantized_img_path_list.sort()

score_list = []
for i in quantized_img_path_list:
    quantized_img = np.array(Image.open(i),'f')
    quantized_width = quantized_img.shape[0]
    quantized_height = quantized_img.shape[1]*quantized_img.shape[2]
    quantized_img.resize((quantized_width,quantized_height))
    score = sporco.metric.gmsd(temp_img, quantized_img)
    score_list.append(score)
print(score_list)

# save gmsd score to csv file
csvfile = "sky_gmsd.csv"
with open(csvfile, "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    for val in score_list:
        writer.writerow([val])