class Solution(object):
    def myPow(self, x, n):
        """
        :type x: float
        :type n: int
        :rtype: float
        """
        if n == 0:
            return 1.0
        if x == 0:
            return 0.0

        if n < 0:
            x = 1 / x
            n = -n

        result = 1.0
        base = x
        exp = n

        while exp > 0:
            if exp & 1:
                result *= base
            base *= base
            exp >>= 1

        return result
