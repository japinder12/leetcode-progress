class Solution(object):
    def isValid(self, s):
        """
        :type s: str
        :rtype: bool
        """
        stack = []
        pair = {')': '(', ']': '[', '}': '{'}
        
        for ch in s:
            if ch in pair.values():
                stack.append(ch)
            elif ch in pair:
                if not stack or stack[-1] != pair[ch]:
                    return False
                stack.pop()
        return not stack