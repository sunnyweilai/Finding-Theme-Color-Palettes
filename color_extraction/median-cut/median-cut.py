from PIL import Image
from colorthief import ColorThief

# use PIL (quantize) to extract
# if __name__ == "__main__":
#     im = Image.open("img/universe.jpg")
#     im2 = im.quantize(16)
#     im2.show()

# use colorthief (median-cut algorithm) to extract
color_thief = ColorThief('img/universe.jpg')
# get the dominant color
dominant_color = color_thief.get_color(quality=1)
# build a color palette
palette = color_thief.get_palette(color_count=6)
print(palette)