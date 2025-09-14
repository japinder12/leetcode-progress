class Solution(object):
    def spellchecker(self, wordlist, queries):
        """
        :type wordlist: List[str]
        :type queries: List[str]
        :rtype: List[str]
        """
        vowels = set('aeiou')

        def devowel(w):
            w = w.lower()
            return ''.join('*' if ch in vowels else ch for ch in w)

        exact = set(wordlist)
        case_map = {}
        vowel_map = {}

        for w in wordlist:
            lw = w.lower()
            case_map.setdefault(lw, w)
            vowel_map.setdefault(devowel(w), w)

        ans = []
        for q in queries:
            if q in exact:
                ans.append(q)
                continue
            lq = q.lower()
            if lq in case_map:
                ans.append(case_map[lq])
                continue
            dv = devowel(q)
            ans.append(vowel_map.get(dv, ""))
        return ans
