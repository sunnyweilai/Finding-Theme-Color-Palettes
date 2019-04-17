"""
Build the RGB color object in order to do the color quantization
"""
class RGB_Color(object):

    def __init__(self, red = 0, green = 0, blue = 0, alpha = None):
        """
        initialize color
        :param red:
        :param green:
        :param blue:
        :param alpha:
        """
        self.red = red
        self.green = green
        self.blue = blue
        self.alpha = alpha