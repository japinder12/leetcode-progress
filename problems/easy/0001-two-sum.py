# Time: O(n)
# Space: O(n)

class Solution(object):
    def twoSum(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        """
        hm = {} # val : i
        for i, n in enumerate(nums):
            diff = target - n
            if diff in hm:
                return [hm[diff], i]
            hm[n] = i
        return