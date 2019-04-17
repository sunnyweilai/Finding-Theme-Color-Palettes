"""
Build the L*a*b* color object in order to do the color quantization
"""
class LAB_Color(object):

    def __init__(self, LAB = (0,0,0), alpha = None):
        """
        initialize
        :param L:
        :param A:
        :param B:
        :param alpha:
        """
        self.L = LAB[0]
        self.A = LAB[1]
        self.B = LAB[2]
        self.alpha = alpha
