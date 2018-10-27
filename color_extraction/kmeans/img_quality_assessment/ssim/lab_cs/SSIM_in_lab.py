import numpy as np
import csv
import math
from sklearn.cluster import KMeans
import scipy.misc
from skimage import color,data,img_as_uint
from skimage.measure import compare_ssim
from quantization_sky_float64 import testimg_list,rescale_ori


# compare MSSIM
score_list = []
for i in testimg_list:
    score = compare_ssim(rescale_ori, i, multichannel=True)
    score_list.append(score)
print(score_list)

# save ssim score to csv file
csvfile = "ssim_lab_v1.csv"
with open(csvfile, "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    for val in score_list:
        writer.writerow([val])







