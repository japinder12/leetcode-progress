class Solution(object):
    def findClosest(self, x, y, z):
        """
        :type x: int
        :type y: int
        :type z: int
        :rtype: int
        """
        dx = abs(x - z)
        dy = abs(y - z)
        if dx < dy:
            return 1
        if dy < dx:
            return 2
        return 0
