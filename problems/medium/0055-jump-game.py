class Solution(object):
    def canJump(self, nums):
        """
        :type nums: List[int]
        :rtype: bool
        """
        dp = [False for i in range(len(nums))]
        dp[0] = True

        for i in range(len(nums)):
            if dp[i]:
                for j in range(i, i + nums[i] + 1):
                    if j < len(nums):
                        dp[j] = True

        return dp[len(nums) - 1]
