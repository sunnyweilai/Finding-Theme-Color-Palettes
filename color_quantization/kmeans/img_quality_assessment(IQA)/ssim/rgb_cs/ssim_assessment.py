"""
image quality assessment (IQA) of the quantized images and the original image in RGB color space
----- method: SSIM
----- version 1.0 ("ssim" library written by jterrace)
----- https://github.com/jterrace/pyssim
"""

from PIL import Image
import ssim
import glob
import csv


# ---- obtain the original image and quantized images with different numbers of colors
temp_img = Image.open('../../../../img/sky.jpg')
quantized_img_path_list = []
quantized_img_path_list = glob.glob(r'../../../img/sky/rgb_cs/quantized_img/*.png')
quantized_img_path_list.sort()
print(quantized_img_path_list)

# ---- ssim evaluation
score_list = []
for i in quantized_img_path_list:
    img = Image.open(i)
    score = ssim.compute_ssim(img,temp_img)
    score_list.append(score)


# ---- save ssim score to csv file
csvfile = "sky_ssim.csv"
with open(csvfile, "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    for val in score_list:
        writer.writerow([val])

