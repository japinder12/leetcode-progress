class Solution(object):
    def insert(self, intervals, newInterval):
        """
        :type intervals: List[List[int]]
        :type newInterval: List[int]
        :rtype: List[List[int]]
        """
        result = []
        i, n = 0, len(intervals)
        new_start, new_end = newInterval

        while i < n and intervals[i][1] < new_start:
            result.append(intervals[i])
            i+=1
        
        while i < n and intervals[i][0] <= new_end:
            new_start = min(new_start, intervals[i][0])
            new_end = max(new_end, intervals[i][1])
            i+=1
        result.append([new_start, new_end])

        while i < n:
            result.append(intervals[i])
            i+=1

        return result
    