"""
image quality assessment (IQA) of the quantized images and the original image in l* channel of L*a*b* color space
----- method: SSIM
----- version 1.0 (skimage library)
----- http://scikit-image.org/docs/dev/auto_examples/transform/plot_ssim.html
"""
"""
Inspired by the PSNR computation, we can we can only compute SSIM for the L* channel of images. 
Since luminance plane consists of significant information 
in the image the evaluation score obtained is closer to human vision judgement.
"""

import csv
from skimage.measure import compare_ssim

# import the original and quantized image arrays in L*a*b* color space
from quantization_sky_float64 import testimg_list,rescale_ori

# ---- extract L* channel of the original image
L_ori = rescale_ori[:,:,0]


# ---- compare MSSIM
score_list = []
for i in testimg_list:
    L_test = i[:,:,0]
    score = compare_ssim(L_ori, L_test, multichannel=False)
    score_list.append(score)
print(score_list)

# ---- save ssim score to csv file
csvfile = "sky_ssim_in_L_lab.csv"
with open(csvfile, "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    for val in score_list:
        writer.writerow([val])







