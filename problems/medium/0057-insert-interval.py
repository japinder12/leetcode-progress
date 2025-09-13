class Solution(object):
    def insert(self, intervals, newInterval):
        """
        :type intervals: List[List[int]]
        :type newInterval: List[int]
        :rtype: List[List[int]]
        """
        res = []
        i = 0
        n = len(intervals)
        s, e = newInterval
        # add all before
        while i < n and intervals[i][1] < s:
            res.append(intervals[i])
            i += 1
        # merge overlaps
        while i < n and intervals[i][0] <= e:
            s = min(s, intervals[i][0])
            e = max(e, intervals[i][1])
            i += 1
        res.append([s, e])
        # add rest
        while i < n:
            res.append(intervals[i])
            i += 1
        return res

