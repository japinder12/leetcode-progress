class Solution(object):
    def dailyTemperatures(self, temperatures):
        """
        :type temperatures: List[int]
        :rtype: List[int]
        """
        n = len(temperatures)
        answer = [0] * n
        stk = [] # track indices

        for i in range(len(temperatures)):
            while stk and temperatures[stk[-1]] < temperatures[i]:
                idx = stk.pop()
                answer[idx] = i-idx
            stk.append(i)

        return answer
    