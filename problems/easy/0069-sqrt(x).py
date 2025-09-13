class Solution(object):
    def mySqrt(self, x):
        """
        :type x: int
        :rtype: int
        """
        a = x
        while a * a > x:
            a = (a + x / a) / 2
        return int(a)