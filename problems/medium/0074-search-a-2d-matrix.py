class Solution(object):
    def searchMatrix(self, matrix, target):
        """
        :type matrix: List[List[int]]
        :type target: int
        :rtype: bool
        """
        n, m = len(matrix), len(matrix[0])
        l, r = 0, m*n-1
        while l <= r:
            mid = (l+r) // 2
            num = matrix[mid // m][mid % m]

            if num == target:
                return True
            elif num < target:
                l = mid + 1
            else:
                r = mid - 1
        
        return False
    