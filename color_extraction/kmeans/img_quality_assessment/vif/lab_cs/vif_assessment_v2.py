import numpy as np
import scipy.misc
from PIL import Image
import glob
import csv
import math
from vif_function import vifp_mscale
from skimage import color

"""convert image into lab color space and convert back (in order to compare)"""
# lab_raster = color.rgb2lab(original_img)
# rgb_raster = color.lab2rgb(lab_raster) * 255
# rgb_image = Image.fromarray(rgb_raster.astype(np.uint8))
# rgb_image.save("temp_image.png" )

original_img = scipy.misc.imread('../../../../img/sky.jpg')
lab_original_img = color.rgb2lab(original_img)

quantized_img_path_list = []
quantized_img_path_list = glob.glob(r'../../../img/sky/lab_cs/quantized_img/*.png')
quantized_img_path_list.sort()


score_list = []
for i in quantized_img_path_list:
    quantized_img = scipy.misc.imread(i)
    lab_quantized_img = color.rgb2lab(quantized_img)
    score = vifp_mscale(lab_original_img, lab_quantized_img)
    score_list.append(score)
print(score_list)

# save vif score to csv file
csvfile = "lab_sky_vif.csv"
with open(csvfile, "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    for val in score_list:
        writer.writerow([val])