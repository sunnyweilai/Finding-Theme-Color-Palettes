import numpy as np
from sklearn.cluster import KMeans
from sklearn import metrics
import scipy.misc
import matplotlib.pyplot as plt
import  matplotlib.colors as mcolors
from PIL import Image
import ssim
import glob

temp_img = Image.open('../img/sky.jpg')

quantized_img_path_list = []
quantized_img_path_list = glob.glob(r'img/sky/quantized_img/*.png')
quantized_img_path_list.sort()
print(quantized_img_path_list)

for i in quantized_img_path_list:
    img = Image.open(i)
    score = ssim.compute_ssim(img,temp_img)
    print(score)