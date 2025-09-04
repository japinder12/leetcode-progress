class Solution(object):
    def reverse(self, x):
        """
        :type x: int
        :rtype: int
        """
        INT_MIN, INT_MAX = -2**31, 2**31 - 1
        rev = int(str(abs(x))[::-1]) * (-1 if x < 0 else 1)
        return rev if INT_MIN <= rev <= INT_MAX else 0
