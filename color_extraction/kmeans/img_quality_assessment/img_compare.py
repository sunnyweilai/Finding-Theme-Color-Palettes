import numpy as np
import scipy.misc
from PIL import Image
import glob
import csv
import math
from skimage import color

original = scipy.misc.imread('../../img/sky.jpg')
print(original)
temp = scipy.misc.imread('vif/lab_cs/temp_image.png')
print(temp)