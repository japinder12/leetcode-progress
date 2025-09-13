class Solution(object):
    def merge(self, intervals):
        """
        :type intervals: List[List[int]]
        :rtype: List[List[int]]
        """
        intervals.sort(key= lambda x: x[0])
        merged = [intervals[0]]
        for start, end in intervals[1:]:
            prev_start, prev_end = merged[-1]
            if prev_end >= start:
                merged[-1][1] = max(prev_end, end)
            else:
                merged.append([start,end])
        return merged
