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

original_img = np.array(Image.open('../../../../img/sky.jpg'),'f')

quantized_img_path_list = []
quantized_img_path_list = glob.glob(r'../../../img/sky/lab_cs/quantized_img/*.png')
quantized_img_path_list.sort()


score_list = []
for i in quantized_img_path_list:
    quantized_img = np.array(Image.open(i),'f')
    score = vifp_mscale(original_img, quantized_img)
    score_list.append(score)
print(score_list)

# save vif score to csv file
csvfile = "sky_vif_with_original.csv"
with open(csvfile, "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    for val in score_list:
        writer.writerow([val])