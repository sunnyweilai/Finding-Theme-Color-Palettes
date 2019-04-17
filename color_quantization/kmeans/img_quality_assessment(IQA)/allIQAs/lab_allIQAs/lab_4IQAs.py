import sporco.metric
from skimage.measure import compare_ssim
from vif_function import vifp_mscale
import math
import numpy as np




# -----------------compute PSNR in RGB
def psnr_list(original, quantized_list):
    # ---- PSNR method
    def psnr(img1, img2):
        mse = np.mean((img1 - img2) ** 2)
        if mse == 0:
            return 100
        # ---- 16 bits per pixel in lab color space
        PIXEL_MAX = 1
        return 10 * math.log10((PIXEL_MAX) ** 2 / mse)
    PSNR_score_list = []
    L_PSNR_score_list = []
    for i in quantized_list:
        score = psnr(original, i)
        PSNR_score_list.append(score)

        L_score = psnr(original[:,:,0], i[:,:,0])
        L_PSNR_score_list.append(L_score)

    return  PSNR_score_list, L_PSNR_score_list


# ---------------- compute mean SSIM
def ssim_list(original, quantized_list):
    SSIM_score_list = []
    L_SSIM_score_list = []
    for i in quantized_list:
        score = compare_ssim(original, i, multichannel=True)
        SSIM_score_list.append(score)

        L_score = compare_ssim(original[:,:,0], i[:,:,0], multichannel=False)
        L_SSIM_score_list.append(L_score)
    return SSIM_score_list, L_SSIM_score_list


# ---------------- compute VIF
def vif_list(original, quantized_list):
    VIF_score_list = []
    for i in quantized_list:
        score = vifp_mscale(original, i)
        VIF_score_list.append(score)
    return VIF_score_list


# --------------- compute GMSD
def gmsd_list(original, quantized_list):
    # ---- resize original image array to 2d
    rgb_temp_width = original.shape[0]
    rgb_temp_height = original.shape[1] * original.shape[2]
    original.resize((rgb_temp_width, rgb_temp_height))

    # --------------- compute GMSD
    GMSD_score_list = []
    for i in quantized_list:
        rgb_quantized_width = i.shape[0]
        rgb_quantized_height = i.shape[1] * i.shape[2]
        i.resize((rgb_quantized_width, rgb_quantized_height))
        score = sporco.metric.gmsd(original, i)
        GMSD_score_list.append(score)
    return GMSD_score_list