import sys

from PIL import Image
from color import Color
from quantizer import OctreeQuantizer


def main():
    image = Image.open('../img/universe.jpg')
    pixels = image.load()
    width,height = image.size

    octree = OctreeQuantizer()

    # add colors to octree
    for j in xrange(height):
        for i in xrange(width):
            octree.add_color(Color(*pixels[i, j]))

    # 256 colors for 8 bits per pixel output image
    palette = octree.make_palette(256)

    # make palette for 256 colors and save it to files
    palette_image = Image.new('RGB', (16, 16))
    palette_pixels = palette_image.load()
    for i, color in enumerate(palette):
        palette_pixels[i % 16, i / 16] = (color.red, color.green, color.blue)
    palette_image.save('universe_palette.png')

    # save output image
    out_image = Image.new('RGB', (width, height))
    out_pixels = out_image.load()
    for j in xrange(height):
        for i in xrange(width):
            index = octree.get_palette_index(Color(*pixels[i, j]))
            color = palette[index]
            out_pixels[i, j] = (color.red, color.green, color.blue)
    out_image.save('universe_out.png')


if __name__ == '__main__':
    main()