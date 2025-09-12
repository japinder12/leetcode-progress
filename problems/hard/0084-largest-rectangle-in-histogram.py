class Solution(object):
    def largestRectangleArea(self, heights):
        """
        :type heights: List[int]
        :rtype: int
        """
        hs = heights + [0]
        n = len(hs)
        stk = []
        max_area = 0
        for i in range(n): 
            curr = hs[i]
            while stk and curr < hs[stk[-1]]:
                temp = stk.pop()
                temp_h = hs[temp]
                if not stk:
                    width = i
                else:
                    width = i - stk[-1] - 1
                max_area = max(max_area, width * temp_h)
            stk.append(i)
        return max_area
