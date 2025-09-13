class Solution(object):
    def lengthOfLastWord(self, s):
        """
        :type s: str
        :rtype: int
        """
        i = len(s) - 1
        # skip trailing spaces
        while i >= 0 and s[i] == ' ':
            i -= 1
        if i < 0:
            return 0
        # count last word
        j = i
        while j >= 0 and s[j] != ' ':
            j -= 1
        return i - j

