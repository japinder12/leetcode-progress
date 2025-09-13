class Solution(object):
    def canJump(self, nums):
        """
        :type nums: List[int]
        :rtype: bool
        """
        max_reach = 0
        for i, jump in enumerate(nums):
            if i > max_reach:
                return False
            if i + jump > max_reach:
                max_reach = i + jump
        return True

