class Solution(object):
    def maxSubArray(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        maxSum = float('-inf')
        currSum = 0
        for i in range(len(nums)):
            currSum += nums[i]
            maxSum = max(maxSum, currSum)
            currSum = max(currSum, 0)
        return maxSum