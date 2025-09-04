class Solution(object):
    def generateParenthesis(self, n):
        """
        :type n: int
        :rtype: List[str]
        """
        dp = [[] for _ in range(n + 1)]
        dp[0] = [""]  # important base case
        for k in range(1, n + 1):
            combos = []
            for c in range(k):
                for left in dp[c]:
                    for right in dp[k - 1 - c]:
                        combos.append(f"({left}){right}")
            dp[k] = combos
        return dp[n]
