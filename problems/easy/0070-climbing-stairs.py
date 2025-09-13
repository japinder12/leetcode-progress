class Solution(object):
    def climbStairs(self, n):
        """
        :type n: int
        :rtype: int
        """
        # if n <= 2:
        #     return n
        # a, b = 1, 2
        # for _ in range(3, n + 1):
        #     a, b = b, a + b
        # return b

        dp = []

        for i in range(0, n+1):
            dp.append(-1)
        
        dp[0] = 1
        dp[1] = 1

        for i in range(2, n+1):
            dp[i] = dp[i-1] + dp[i-2]

        return dp[n]
    