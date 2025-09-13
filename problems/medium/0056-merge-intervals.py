class Solution(object):
    def merge(self, intervals):
        """
        :type intervals: List[List[int]]
        :rtype: List[List[int]]
        """
        if not intervals:
            return []
        intervals.sort(key=lambda x: x[0])
        merged = [intervals[0][:]]
        for s, e in intervals[1:]:
            last = merged[-1]
            if s <= last[1]:
                if e > last[1]:
                    last[1] = e
            else:
                merged.append([s, e])
        return merged

