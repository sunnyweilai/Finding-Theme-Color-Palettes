import numpy as np
import scipy.misc
from PIL import Image
import glob
import csv
import math
from vif_function import vifp_mscale


temp_img = np.array(Image.open('../../../../img/sky.jpg'),'f')
quantized_img_path_list = []
quantized_img_path_list = glob.glob(r'../../../img/sky/rgb_cs/quantized_img/*.png')
quantized_img_path_list.sort()


score_list = []
for i in quantized_img_path_list:
    quantized_img = np.array(Image.open(i),'f')
    score = vifp_mscale(temp_img, quantized_img)
    score_list.append(score)

# save vif score to csv file
csvfile = "sky_vif.csv"
with open(csvfile, "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    for val in score_list:
        writer.writerow([val])