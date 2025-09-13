from collections import Counter

class Solution(object):
    def maxFreqSum(self, s):
        """
        :type s: str
        :rtype: int
        """
        vowels = set("aeiou")
        cnt = Counter(c for c in s.lower() if c.isalpha())
        max_v = max([cnt[c] for c in vowels] or [0])
        max_c = max([v for c, v in cnt.items() if c not in vowels] or [0])
        return max_v + max_c
