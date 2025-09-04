class Solution(object):
    def maxArea(self, height):
        """
        :type height: List[int]
        :rtype: int
        """
        maxArea = 0
        leftPtr = 0
        rightPtr = len(height) -1

        maxArea = 0

        while leftPtr < rightPtr:
            width = rightPtr - leftPtr
            currArea = min(height[leftPtr], height[rightPtr]) * width
            maxArea = max(maxArea, currArea)

            if height[leftPtr] < height[rightPtr]:
                leftPtr += 1
            else:
                rightPtr -= 1

        return maxArea