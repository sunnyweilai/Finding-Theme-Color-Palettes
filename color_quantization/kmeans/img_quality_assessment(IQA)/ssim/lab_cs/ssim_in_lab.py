"""
image quality assessment (IQA) of the quantized images and the original image in L*a*b* color space
----- method: SSIM
----- version 1.0 (skimage library)
----- http://scikit-image.org/docs/dev/auto_examples/transform/plot_ssim.html
"""

import csv
from skimage.measure import compare_ssim

# import the original and quantized image arrays in L*a*b* color space
from quantization_sky_float64 import testimg_list,rescale_ori


# ---- compare mean SSIM (MSSIM)
score_list = []
for i in testimg_list:
    score = compare_ssim(rescale_ori, i, multichannel=True)
    score_list.append(score)
print(score_list)

# ---- save ssim score to csv file
csvfile = "sky_ssim_in_L_lab.csv"
with open(csvfile, "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    for val in score_list:
        writer.writerow([val])







