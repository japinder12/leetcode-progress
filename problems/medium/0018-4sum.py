class Solution(object):
    def fourSum(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[List[int]]
        """
        n = len(nums)
        checked = set()
        ans = set()
        for i in range(n):
            for j in range(i+1, n):
                for k in range(j+1, n):
                    lastNum = target - nums[i] - nums[j] - nums[k]
                    if lastNum in checked:
                        arr = sorted([nums[i], nums[j], nums[k], lastNum])
                        ans.add((arr[0], arr[1], arr[2], arr[3]))
            checked.add(nums[i])
        return ans
        