"""
image quality assessment (IQA) of the quantized images and the original image in L* channel of L*a*b* color space
----- method: PSNR
"""
"""
Human eyes are most sensitive to luma information which represents brightness in an image. 
With this consideration, in L*a*b* color space we can separate L* channel and only compute PSNR on it
"""

import sys
sys.path.insert(0, '/anaconda2/envs/Lai_Project/color_quantization/kmeans/img_quality_assessment(img_quality_assessment(img_quality_assessment(IQA)))/psnr/lab_cs')

from quantization_sky_float64 import testimg_list, rescale_ori, psnr
import csv


# ---- compare PSNR
score_list = []
for i in testimg_list:

    # ---- compute the L channel of the original and quantzied images
    score = psnr(rescale_ori[:,:,0], i[:,:,0])
    score_list.append(score)
print(score_list)

# ---- save PSNR score to csv file
csvfile = "sky_psnr_in_L_lab.csv"
with open(csvfile, "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    for val in score_list:
        writer.writerow([val])









