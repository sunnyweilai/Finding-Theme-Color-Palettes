import numpy as np
import scipy.misc
from PIL import Image
import glob
import csv
import math
import skimage.measure as skm



temp_img = np.array(Image.open('../../../img/sky.jpg'))
quantized_img_path_list = []
quantized_img_path_list = glob.glob(r'../../img/sky/quantized_img/*.png')
quantized_img_path_list.sort()


score_list = []
for i in quantized_img_path_list:
    quantized_img = np.array(Image.open(i))
    score = skm.compare_psnr(temp_img, quantized_img)
    score_list.append(score)
print(score_list)