class LAB_Color(object):

    # def __init__(self, colors, alpha=None):
    #     self.colors = colors or []
    #     self.L = [l[0] for l in colors]
    #     self.A = [a[1] for a in colors]
    #     self.B = [b[2] for b in colors]
    #     self.alpha = [alpha[3] for alpha in colors]
    #
    #
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
